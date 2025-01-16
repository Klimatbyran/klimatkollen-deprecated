import styled from 'styled-components'
import { useTranslation } from 'next-i18next'
import { devices } from '../../utils/devices'

import MailIcon from '../../public/icons/icon_mail_circle.svg'
import XLogo from '../../public/icons/some/x_white.svg'
import LinkedInLogo from '../../public/icons/some/linkedin_white.svg'
import GitHubLogo from '../../public/icons/some/github.svg'
import DiscordLogo from '../../public/icons/some/discord.svg'
import InstagramLogo from '../../public/icons/some/Instagram_Glyph_Black.svg'
import FacebookLogo from '../../public/icons/some/facebook.svg'

const ContactList = styled.ul`
  list-style: none;

  @media only screen and (${devices.smallMobile}) {
    display: grid;
    grid-template-rows: repeat(2, 1fr);
    grid-template-columns: repeat(2, 1fr);
    justify-items: center;
  }
`

const ContactListItem = styled.li`
  width: 128px;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 16px;
`

const ContactLink = styled.a`
  text-decoration: none;
  font-weight: bold;
  font-size: 13px;
`

type SocialListItemProps = {
  link: string
  text: string
  Icon: React.FC;
}

export function SocialListItem({
  link, text, Icon,
}: SocialListItemProps): JSX.Element {
  return (
    <ContactListItem>
      <Icon />
      <ContactLink href={link} target="_blank" rel="noreferrer">
        {text}
      </ContactLink>
    </ContactListItem>
  )
}

function SocialList() {
  const { t } = useTranslation(['common'])
  return (
    <ContactList>
      <SocialListItem
        link="mailto:hej@klimatkollen.se"
        text={t('footer.email-us')}
        Icon={MailIcon}
      />
      <SocialListItem
        link="https://twitter.com/klimatkollen"
        text="X (Twitter)"
        Icon={XLogo}
      />
      <SocialListItem
        link="https://www.linkedin.com/company/klimatkollen/"
        text="LinkedIn"
        Icon={LinkedInLogo}
      />
      <SocialListItem
        link="https://github.com/Klimatbyran/"
        text="GitHub"
        Icon={GitHubLogo}
      />
      <SocialListItem
        Icon={DiscordLogo}
        link="https://discord.gg/FPX9yqYAmk"
        text="Discord"
      />
      <SocialListItem
        Icon={InstagramLogo}
        link="https://instagram.com/klimatkollen.se"
        text="Instagram"
      />
      <SocialListItem
        Icon={FacebookLogo}
        link="https://www.facebook.com/klimatkollen/"
        text="Facebook"
      />
    </ContactList>
  )
}

export default SocialList
