from yt_dlp.extractor.youtube import YoutubeIE
from yt_dlp.networking import Request

# ⚠ The class name must end in "IE"
class YoutubeMusicAccessTokenAuthHandlerIE(YoutubeIE, plugin_name='yt_access_token'):
    _NETRC_MACHINE = 'youtube'
    auth: str = ""

    def _inject_auth_header(self, request: Request):
        """
        Inject the authentication header into the request.
        """
        # Remove conflicting headers
        request.headers.pop('X-Goog-PageId', None)
        request.headers.pop('X-Goog-AuthUser', None)

        # Warn if cookies and OAuth2 are both being used
        if 'Authorization' in request.headers:
            self.report_warning(
                'Youtube cookies have been provided, but OAuth2 is being used. '
                'If you encounter problems, stop providing Youtube cookies to yt-dlp.')
            request.headers.pop('Authorization', None)
            request.headers.pop('X-Origin', None)

        # Remove unused headers
        request.headers.pop('X-Youtube-Identity-Token', None)

        # Inject the authorization header
        authorization_header = {'Authorization': f'Bearer {self.auth}'}
        request.headers.update(authorization_header)

    def _perform_login(self, username, password):
        """
        Perform login by setting the auth token.
        """
        self.auth = username

    def _create_request(self, *args, **kwargs):
        """
        Create a request and inject authentication header.
        """
        request = super()._create_request(*args, **kwargs)
        self._inject_auth_header(request)
        return request
