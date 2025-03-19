/* eslint-disable react/jsx-props-no-spreading */
import type { AppProps } from 'next/app'
import Head from 'next/head'
import Script from 'next/script'
import CookieConsent from 'react-cookie-consent'
import { GetStaticProps, NextPage } from 'next'
import { ReactElement, ReactNode } from 'react'
import { appWithTranslation, useTranslation } from 'next-i18next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { StyleSheetManager } from 'styled-components'
import isPropValid from '@emotion/is-prop-valid'

import '@fontsource-variable/dm-sans'
import '../styles/globals.css'
import Theme, { colorTheme } from '../Theme'
import nextI18nextConfig from '../next-i18next.config'

type NextPageWithLayout = NextPage & {
  getLayout?: (page: ReactElement) => ReactNode
}

type AppPropsWithLayout = AppProps & {
  Component: NextPageWithLayout
}

function MyApp({ Component, pageProps }: AppPropsWithLayout) {
  const getLayout = Component.getLayout ?? ((page) => page)
  const { t } = useTranslation()

  return (
    <StyleSheetManager shouldForwardProp={isPropValid}>
      <Script
        strategy="lazyOnload"
        src={`https://www.googletagmanager.com/gtag/js?id=${process.env.NEXT_PUBLIC_GOOGLE_ANALYTICS}`}
      />

      <Script strategy="lazyOnload" id="gtag">
        {`
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', '${process.env.NEXT_PUBLIC_GOOGLE_ANALYTICS}', {
        page_path: window.location.pathname,
        });
    `}
      </Script>
      <Head>
        <title>Klimatkollen</title>
        {/* https://favicon.io/favicon-converter/ */}
        <link rel="icon" href="/favicon.ico" />
        <link
          rel="icon"
          type="image/png"
          sizes="16x16"
          href="/favicons/favicon-16x16.png"
        />
        <link
          rel="icon"
          type="image/png"
          sizes="32x32"
          href="/favicons/favicon-32x32.png"
        />
        <link
          rel="icon"
          type="image/png"
          sizes="192x192"
          href="/favicons/favicon-192x192.png"
        />
        <link
          rel="icon"
          type="image/png"
          sizes="512x512"
          href="/favicons/favicon-512x512.png"
        />
        <meta
          property="og:image"
          content="https://klimatkollen.se/images/social-picture.png"
        />
        <meta property="twitter:card" content="summary_large_image" />
        <meta
          property="twitter:image"
          content="https://klimatkollen.se/images/social-picture.png"
        />
      </Head>
      <Theme>
        <CookieConsent
          location="bottom"
          buttonText={t('common:actions.ok')}
          style={{ background: colorTheme.newColors.black2 }}
          buttonStyle={{
            backgroundColor: colorTheme.newColors.blue2,
            fontSize: '13px',
          }}
          expires={150}
        >
          {t('common:cookieBanner')}
        </CookieConsent>
        {getLayout(<Component {...pageProps} />)}
      </Theme>
    </StyleSheetManager>
  )
}

export const getStaticProps: GetStaticProps = async ({ locale }) => ({
  props: {
    ...(await serverSideTranslations(locale as string, ['common'])),
  },
})

export default appWithTranslation(MyApp, nextI18nextConfig)
