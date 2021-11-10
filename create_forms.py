from popsss.tests.factories import (
    ContributorReleaseFormAttachmentFactory,
    ContributorReleaseFormFactory,
    ContributorReleaseFormLogFactory,
    ProfileFactory,
    ReleaseFormAddressLinkFactory,
    SiteFactory,
    SiteFormFactory,
    SiteFormLogFactory,
    SiteFormTemplateFactory,
    UserFactory,
)
from tg import request
from unittest.mock import patch

request.environ["REMOTE_ADDR"] = "stubbed"

@patch('popsss.model.auth.validate_email', side_effect=lambda email: email)
def _initialise_forms(_):
    for num in range(2):
        site = SiteFactory(url=f"test{num}")
        site_id = site.site_id
        user = UserFactory(site_id=site_id)
        profile = ProfileFactory(site=site, user=user)

        for _ in range(3):
            site_form_template = SiteFormTemplateFactory(site=site)
            site_form = SiteFormFactory(profile=profile, template=site_form_template)
            SiteFormLogFactory(
                site_form_id=site_form.site_form_id, event_user_id=user.user_id
            )

            release_form = ContributorReleaseFormFactory(
                activity=site, template__activity=site
            )
            ReleaseFormAddressLinkFactory(release_form=release_form)
            ContributorReleaseFormLogFactory(
                release_form_id=release_form.release_form_id, event_user_id=user.user_id
            )
            ContributorReleaseFormAttachmentFactory(release_form=release_form)
