import js from '@eslint/js'
import globals from 'globals'
import reactHooks from 'eslint-plugin-react-hooks'
import reactRefresh from 'eslint-plugin-react-refresh'

export default [
  { ignores: ['dist', 'node_modules'] },
  {
    files: ['**/*.{js,jsx,mjs}'],
    languageOptions: {
      ecmaVersion: 2022,
      globals: { ...globals.browser, ...globals.node },
      parserOptions: { ecmaFeatures: { jsx: true }, sourceType: 'module' },
    },
    plugins: { 'react-hooks': reactHooks, 'react-refresh': reactRefresh },
    rules: {
      ...js.configs.recommended.rules,
      ...reactHooks.configs.recommended.rules,
      // JSX identifiers count as uses (no eslint-plugin-react installed).
      'no-unused-vars': ['error', { varsIgnorePattern: '^(React|[A-Z_])', args: 'none' }],
      'react-refresh/only-export-components': 'off',
      // React-Compiler advisory rules. They flag the standard
      // "load data on mount" effect and Date.now() used deliberately to
      // create a fresh remount key when a link is clicked; neither is a bug
      // here, so they are off rather than rewriting working pages.
      'react-hooks/set-state-in-effect': 'off',
      'react-hooks/purity': 'off',
    },
  },
]
