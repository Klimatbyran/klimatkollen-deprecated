module.exports = {
  extends: [
    'airbnb',
    'airbnb/hooks',
    'plugin:@typescript-eslint/recommended',
    'plugin:jsx-a11y/recommended',
    'plugin:@next/next/recommended',
  ],
  parser: '@typescript-eslint/parser',
  parserOptions: {
    ecmaVersion: 2023,
    sourceType: 'module',
    ecmaFeatures: {
      jsx: true,
    },
  },
  env: {
    browser: true,
    node: true,
    es6: true,
  },
  plugins: ['@typescript-eslint', 'jsx-a11y'],
  rules: {
    // project-specific rules or overrides
    semi: ['error', 'never'],
    'import/no-unresolved': 'off',
    'import/extensions': 'off',
    'max-len': ['error', { code: 150 }],
    'react/jsx-filename-extension': [2, { extensions: ['.js', '.jsx', '.ts', '.tsx'] }],
    'react/require-default-props': 'off', // fixme revisit and refactor files when there's time to spare
    'class-methods-use-this': 'off',
    'import/prefer-default-export': 'off', // fixme revisit and refactor files when there's time to spare
    'import/no-extraneous-dependencies': 'off', // fixme revisit and refactor files when there's time to spare
    'react/react-in-jsx-scope': 'off',
    'react/jsx-one-expression-per-line': 'warn',
    'no-restricted-imports': [
      'error',
      {
        paths: [
          {
            name: 'react-i18next',
            message: 'Please import useTranslation from next-i18next.',
          },
        ],
      },
    ],
  },
}
