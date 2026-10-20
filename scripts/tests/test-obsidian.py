#!/usr/bin/env python3
"""Exercise vault provisioning and checks without changing the real vault or using the network."""

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import sys
from unittest.mock import patch

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/obsidian.py"
SPEC = importlib.util.spec_from_file_location("vault_tools", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class VaultChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.vault = Path(self.temp.name)
        (self.vault / ".obsidian/plugins/markdownlint").mkdir(parents=True)
        (self.vault / ".obsidian/plugins/markdownlint/manifest.json").write_text('{}')

    def test_setup_preserves_unowned_settings_and_is_idempotent(self):
        data = self.vault / ".obsidian/plugins/markdownlint/data.json"
        data.write_text('{"other": 42}')
        MODULE.setup(self.vault)
        before = data.read_bytes()
        MODULE.setup(self.vault)
        self.assertEqual(before, data.read_bytes())
        self.assertEqual(json.loads(before)["other"], 42)
        self.assertTrue(json.loads(before)["lintOnSave"])
        self.assertEqual(
            json.loads((self.vault / '.markdownlint.json').read_text()),
            json.loads(MODULE.RULES.read_text()),
        )

    def test_equivalent_json_is_not_reformatted(self):
        MODULE.setup(self.vault)
        for relative in ('.markdownlint.json', '.obsidian/plugins/markdownlint/data.json'):
            target = self.vault / relative
            compact = json.dumps(json.loads(target.read_text()), separators=(',', ':'))
            target.write_text(compact)
            before = target.stat().st_mtime_ns
            MODULE.setup(self.vault)
            self.assertEqual(target.read_text(), compact)
            self.assertEqual(target.stat().st_mtime_ns, before)

    def test_failed_atomic_write_preserves_original_and_cleans_temp_file(self):
        target = self.vault / 'settings.json'
        target.write_text('original')
        with patch.object(Path, 'replace', side_effect=OSError('replace failed')):
            with self.assertRaises(OSError):
                MODULE.write_text(target, 'replacement')
        self.assertEqual(target.read_text(), 'original')
        self.assertEqual(list(self.vault.glob('.lint-*')), [])

    def test_conflicting_rules_do_not_change_plugin_settings(self):
        (self.vault / '.markdownlint.json').write_text('{"default": false}')
        with self.assertRaises(ValueError):
            MODULE.setup(self.vault)
        self.assertFalse((self.vault / '.obsidian/plugins/markdownlint/data.json').exists())

    def test_automated_provision_preserves_plugins_and_snippets(self):
        snapshot = {
            'vaultPath': str(self.vault.resolve()), 'configDir': '.obsidian',
            'syncEnabled': True, 'syncLabel': 'Fully synced',
            'installed': ['other-plugin'], 'enabled': ['other-plugin'],
            'snippets': ['other-snippet'], 'supportsSnippets': True,
        }
        calls = []

        def fake_obsidian(vault, *args):
            calls.append(args)
            if args[0] == 'eval':
                code = args[1]
                if 'setCssEnabledStatus' in code:
                    snapshot['snippets'].append('editor-ruler')
                return '=> ' + json.dumps(snapshot)
            plugin = args[1].split('=', 1)[1]
            if args[0] == 'plugin:install':
                snapshot['installed'].append(plugin)
            elif args[0] == 'plugin:enable':
                snapshot['enabled'].append(plugin)
            elif args[0] == 'plugin:disable':
                snapshot['enabled'].remove(plugin)
            return 'OK'

        state = self.vault / 'private-backups'
        with patch.object(MODULE, 'obsidian', side_effect=fake_obsidian), \
                patch.object(MODULE, 'install_tools') as tools:
            MODULE.provision(self.vault, state)
            before = {p: (p.read_bytes(), p.stat().st_mtime_ns)
                      for p in self.vault.rglob('*') if p.is_file()}
            initial_calls = len(calls)
            for _ in range(10):
                MODULE.provision(self.vault, state)
            after = {
                p: (p.read_bytes(), p.stat().st_mtime_ns)
                for p in self.vault.rglob('*') if p.is_file()
            }
        self.assertEqual(before, after)
        self.assertTrue(all(c[0] == 'eval' and 'JSON.stringify' in c[1]
                            for c in calls[initial_calls:]))
        tools.assert_called()
        self.assertEqual(sum(c[0] == 'plugin:install' for c in calls), 2)
        self.assertEqual(sum(c[0] == 'plugin:disable' for c in calls), 0)
        self.assertEqual(snapshot['enabled'], ['other-plugin', 'custom-note-width', 'markdownlint'])
        self.assertIn('other-snippet', snapshot['snippets'])
        self.assertEqual(
            (self.vault / '.obsidian/snippets/editor-ruler.css').read_text(),
            (MODULE.CONFIG / 'editor-ruler.css').read_text(),
        )

    def test_wrong_vault_stops_before_installation(self):
        snapshot = {'vaultPath': '/different/vault', 'configDir': '.obsidian'}
        with patch.object(MODULE, 'obsidian', return_value='=> ' + json.dumps(snapshot)), \
                patch.object(MODULE, 'install_tools') as tools:
            with self.assertRaises(ValueError):
                MODULE.provision(self.vault, self.vault / 'private-backups')
        tools.assert_not_called()

    def test_incomplete_sync_stops_before_installation(self):
        snapshot = {
            'vaultPath': str(self.vault.resolve()), 'configDir': '.obsidian',
            'syncEnabled': True, 'syncLabel': 'Syncing',
        }
        with patch.object(MODULE, 'obsidian', return_value='=> ' + json.dumps(snapshot)), \
                patch.object(MODULE, 'install_tools') as tools:
            with self.assertRaises(ValueError):
                MODULE.provision(self.vault, self.vault / 'private-backups')
        tools.assert_not_called()

    def test_managed_updates_back_up_previous_rules(self):
        target = self.vault / '.markdownlint.json'
        original = '{"default": false}'
        target.write_text(original)
        backups = self.vault / 'private-backups'
        MODULE.setup(self.vault, backups)
        self.assertEqual([p.read_text() for p in backups.rglob('*.bak')], [original])
        self.assertEqual(json.loads(target.read_text()), json.loads(MODULE.RULES.read_text()))
        before = {p: p.stat().st_mtime_ns for p in backups.rglob('*.bak')}
        target.write_text(original)
        MODULE.setup(self.vault, backups)
        self.assertEqual(before, {p: p.stat().st_mtime_ns for p in backups.rglob('*.bak')})

    def test_path_escape_is_rejected(self):
        with self.assertRaises(ValueError):
            MODULE.targets(self.vault, ['../outside.md'])

    def test_word_rule_and_link_checks(self):
        MODULE.setup(self.vault)
        note = self.vault / 'note.md'
        note.write_text('# Note\n\nRead [target](target.md#section).\n')
        (self.vault / 'target.md').write_text('# Target\n\n## Section\n')
        self.assertEqual(MODULE.check(self.vault, ['note.md']), 0)
        note.write_text('# Note\n\n' + ' '.join(['word'] * 18) + '\n')
        self.assertNotEqual(MODULE.check(self.vault, ['note.md']), 0)
        note.write_text('# Note\n\nRead [target](target.md#missing).\n')
        self.assertNotEqual(MODULE.check(self.vault, ['note.md']), 0)

    def test_word_count_ignores_code_tables_and_link_destinations(self):
        MODULE.setup(self.vault)
        note = self.vault / 'note.md'
        note.write_text('# Note\n\n[Short label](https://example.com/a-very-long-url).\n\n'
                        '```text\n' + 'word ' * 30 + '\n```\n\n'
                        '| Column |\n| --- |\n| ' + 'word ' * 30 + '|\n')
        self.assertEqual(MODULE.check(self.vault, ['note.md']), 0)

    def test_line_length_boundary(self):
        MODULE.setup(self.vault)
        note = self.vault / 'note.md'
        note.write_text('# Note\n\n' + 'a' * 60 + ' ' + 'b' * 59 + '\n')
        self.assertEqual(MODULE.check(self.vault, ['note.md']), 0)
        note.write_text('# Note\n\n' + 'a' * 60 + ' ' + 'b' * 60 + '\n')
        self.assertNotEqual(MODULE.check(self.vault, ['note.md']), 0)

    def test_short_sentences_can_share_paragraphs_and_list_items(self):
        MODULE.setup(self.vault)
        note = self.vault / 'note.md'
        sentence = ' '.join(['Word'] + ['word'] * 9) + '.'
        for prefix in ('', '- '):
            with self.subTest(prefix=prefix):
                note.write_text('# Note\n\n' + prefix + sentence + '\n  ' + sentence + '\n')
                self.assertEqual(MODULE.check(self.vault, ['note.md']), 0)

    def test_sentence_boundary_and_soft_wraps(self):
        MODULE.setup(self.vault)
        note = self.vault / 'note.md'
        note.write_text('# Note\n\n' + ' '.join(['word'] * 17) + '.\n')
        self.assertEqual(MODULE.check(self.vault, ['note.md']), 0)
        note.write_text('# Note\n\n' + ' '.join(['word'] * 9) + '\n'
                        + ' '.join(['word'] * 9) + '.\n')
        self.assertNotEqual(MODULE.check(self.vault, ['note.md']), 0)

    def test_safety_exemption(self):
        MODULE.setup(self.vault)
        note = self.vault / 'note.md'
        note.write_text('# Note\n\n<!-- Safety text preserved verbatim. -->\n'
                        '<!-- markdownlint-disable-next-line LIFE001 -->\n' + 'word ' * 20 + '\n')
        # Strip trailing spaces to isolate the custom rule.
        note.write_text('\n'.join(line.rstrip() for line in note.read_text().splitlines()) + '\n')
        self.assertEqual(MODULE.check(self.vault, ['note.md']), 0)


if __name__ == '__main__':
    unittest.main()
