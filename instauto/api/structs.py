from typing import Tuple, Union, Callable
import time
import enum
import pprint
import random

from .constants import (DEFAULT_SIGNATURE_KEY, DEFAULT_HTTP_ENGINE, DEFAULT_IG_CAPABILITIES, DEFAULT_APP_ID,
                        DEFAULT_IG_VERSION, DEFAULT_BUILD_NUMBER, DEFAULT_ANDROID_RELEASE, DEFAULT_ANDROID_SDK,
                        DEFAULT_CHIPSET, DEFAULT_DEVICE, DEFAULT_DPI, DEFAULT_MANUFACTURER, DEFAULT_MODEL,
                        DEFAULT_RESOLUTION, DEFAULT_SIGNATURE_KEY_V, DEFAULT_ACCEPT, DEFAULT_ACCEPT_ENCODING,
                        DEFAULT_ACCEPT_LANGUAGE, DEFAULT_APP_STARTUP_COUNTRY,
                        DEFAULT_BANDWIDTH_TOTALBYTES_B, DEFAULT_BANDWIDTH_TOTALTIME_MS, DEFAULT_RUR, DEFAULT_WWW_CLAIM,
                        DEFAULT_AUTHORIZATION, DEFAULT_CONNECTION_TYPE, DEFAULT_APP_LOCALE, DEFAULT_DEVICE_LOCALE,
                        DEFAULT_ADS_OPT_OUT, DEFAULT_BLOKS_VERSION_ID, DEFAULT_BLOKS_IS_LAYOUT_RTL)

#: Struct that is used to specify which HTTP method to use
Method = enum.Enum("Method", "GET POST")


class WhichGender(enum.Enum):
    male = 1
    female = 2
    prefer_not_to_say = 3
    other = 4


class Surface(enum.Enum):
    profile = 'following_sheet'
    following_list = 'self_unified_follow_lists'
    follow_list = 'follow_list_page'
    follow_requests = 'follow_requests'


#: Struct that is used to specify where a post should be posted
class WhereToPost(enum.Enum):
    story = 3
    Feed = 4


class IGProfile:
    """Holds all data that is generated by Instagram. For pretty much every request, at least one of the attributes
    is used.

    Attributes
    ----------
    signature_key : str, DEPRECATED
        Key generated by Instagram to sign post requests. Can be extracted from the app. Currently, the actual
        signature key is no longer used for signing actual requests.
    signature_key : str
        The version of the signature key. This key is still sent along with signed requests. Could probably work
        without. TODO: check if we still need to send this along with signed requests / if we have to use the signed
                       request format at all
    http_engine : str,
        Facebook uses a custom HTTP engine, called Liger. This is unlikely to change.
    capabilities: str,
        Not sure what this means on Instagram's side, but it needs to get sent along with all requests. Can change
        overtime. Can be extracted from all requests to the 'logging_client_events' endpoint.
    id : str,
        The app id, presumably a constant.
    version : str,
        The version number of the version of instagram to use.
    build_number : str,
        The build number associated with the version number
    """
    def __init__(self, signature_key: str = None, signature_key_version: str = None, http_engine: str = None, \
                 capabilities: str = None, id: str = None, version: str = None, build_number: str = None):
        self.signature_key = signature_key or DEFAULT_SIGNATURE_KEY
        self.signature_key_version = signature_key_version or DEFAULT_SIGNATURE_KEY_V
        self.http_engine = http_engine or DEFAULT_HTTP_ENGINE
        self.capabilities = capabilities or DEFAULT_IG_CAPABILITIES
        self.id = id or DEFAULT_APP_ID
        self.version = version or DEFAULT_IG_VERSION
        self.build_number = build_number or DEFAULT_BUILD_NUMBER


class DeviceProfile:
    """Holds all data about the android 'phone' that we simulate using.
    Attributes
    ----------
    manufacturer : str,
        The phone manufacturer
    android_sdk_version : str,
        The Android sdk version that is, presumably, used by the Instagram app.
    android_release : str,
        The version of Android that the phone runs on.
    device : str,
        The version name of the phone
    model : str,
        The codename from Samsung under which the phone was build, i.e. for the Galaxy S10E, beyond1.
    dpi : str,
        The DPI of the phone used.
    resolution : tuple[int, int],
        The resolution of the phone.
    chipset:
        The chipset that the phone runs on.
    """
    def __init__(self, manufacturer: str = None, android_sdk_version: str = None, android_release: str = None,
                 device: str = None, model: str = None, dpi: int = None, resolution: Tuple[int] = None, chipset: str
                 = None):
        self.manufacturer = manufacturer or DEFAULT_MANUFACTURER
        self.android_sdk_version = android_sdk_version or DEFAULT_ANDROID_SDK
        self.android_release = android_release or DEFAULT_ANDROID_RELEASE
        self.device = device or DEFAULT_DEVICE
        self.model = model or DEFAULT_MODEL
        self.dpi = dpi or DEFAULT_DPI
        self.resolution = resolution or DEFAULT_RESOLUTION
        self.chipset = chipset or DEFAULT_CHIPSET


class State:
    """Structure that holds a lot of data about the state of a session. It contains mainly header values that need to be
    send along with requests to the API.

    Attributes
    ----------
    www_claim : str,
        Some sort of tracking / identifying header value that is send along with every HTTP request. It is also
        updated in almost all responses received from Instagram's API.
    authorization : str,
        Contains the token used for Bearer authentication.
    mid : str,
        Another tracking / identifying header value. Is also sent along with all requests. Is also updated in every
        response.
    logged_in_account_data : LoggedInAccountData,
        Gets filled as soon as you login. Contains a lot of data about your account.
    """
    def __init__(self, app_startup_country: str = None, device_locale: str = None, app_locale: str = None,
                 bandwidth_totalbytes_b: str = None, bandwidth_totaltime_ms: str =
                 None, connection_type: str = None, accept_language: str = None, accept_encoding: str = None,
                 accept: str = None, ads_opt_out: bool = None, authorization: str = None, www_claim: str = None,
                 rur: str = None, bloks_version_id: str = None, bloks_is_layout_rtl: str = None, **kwargs):
        self.app_startup_country = app_startup_country or DEFAULT_APP_STARTUP_COUNTRY
        self.device_locale = device_locale or DEFAULT_DEVICE_LOCALE
        self.app_locale = app_locale or DEFAULT_APP_LOCALE
        self.bandwidth_totalbytes_b = bandwidth_totalbytes_b or DEFAULT_BANDWIDTH_TOTALBYTES_B
        self.bandwidth_totaltime_ms = bandwidth_totaltime_ms or DEFAULT_BANDWIDTH_TOTALTIME_MS
        self.connection_type = connection_type or DEFAULT_CONNECTION_TYPE
        self.accept_language = accept_language or DEFAULT_ACCEPT_LANGUAGE
        self.accept_encoding = accept_encoding or DEFAULT_ACCEPT_ENCODING
        self.accept = accept or DEFAULT_ACCEPT
        self.ads_opt_out = ads_opt_out or DEFAULT_ADS_OPT_OUT
        self.authorization = authorization or DEFAULT_AUTHORIZATION
        self.www_claim = www_claim or DEFAULT_WWW_CLAIM
        self.rur = rur or DEFAULT_RUR
        self.bloks_version_id = bloks_version_id or DEFAULT_BLOKS_VERSION_ID
        self.bloks_is_layout_rtl = bloks_is_layout_rtl or DEFAULT_BLOKS_IS_LAYOUT_RTL

        self.uuid = None
        self.device_id = None
        self.ad_id = None
        self.session_id = None
        self.phone_id = None
        self.pigeon_session_id = None
        self.created = None
        self.user_id = None
        self.mid = None
        self.direct_region_hint = None
        self.shbid = None
        self.shbts = None
        self.target = None
        self.public_api_key = None
        self.public_api_key_id = None
        self.logged_in_account_data = None

        for k, v in kwargs.items():
            setattr(self, k, v)

    def fill(self, f: Callable) -> None:
        """Initializes all variables that:
            1) do not have a default value to start with;
            2) need a unique generated key on a per-user basis
        Parameters
        ----------
        f : function
            The function that generates the unique keys used throughout.
        """
        self.uuid = f()
        self.device_id = f()
        self.ad_id = f()
        self.session_id = f()
        self.phone_id = f()
        self.pigeon_session_id = f()
        self.created = time.time()
        self.user_id = ""
        self.mid = ""
        self.direct_region_hint = ""
        self.shbid = ""
        self.shbts = ""
        self.target = ""
        self.public_api_key = ""
        self.public_api_key_id = 0
        self.logged_in_account_data = LoggedInAccountData

    @property
    def connection_speed(self) -> str:
        """Randomizes the connection speed."""
        return f"{random.randint(1000, 3700)}kbps"

    @property
    def bandwidth_speed_kbps(self):
        """Randomizes the bandwidth speed"""
        return f"{random.randint(1000, 5000)}.{random.randint(100, 999)}"

    @property
    def android_id(self):
        """Creates an Android id from the device id."""
        return f"android-{self.device_id[9:28].replace('-', '')}"

    @property
    def valid(self) -> bool:
        """Sessions older then 90 days will not work anymore."""
        return self.created + 60 * 60 * 24 * 90 > time.time()

    @property
    def startup_country(self) -> str:
        return self.app_locale.split('_')[-1]

    def __repr__(self):
        return pprint.pformat(vars(self))

    def refresh(self, f: Callable):
        self.uuid = f()
        self.device_id = f()
        self.ad_id = f()
        self.session_id = f()


class LoggedInAccountData:
    """Structure that stores information about the Instagram account"""
    def __init__(self, account_type: int = None, account_badges: list = None, allow_contacts_sync: bool = None,
                 allowed_commenter_type:
    str = None, can_boost_post: bool = None, can_see_organic_insights: bool = None, can_see_primary_country_in_settings: bool = None, full_name:
    str = None, has_anonymous_profile_picture: bool = None, has_placed_orders: bool = None, interop_messaging_user_fbid: int = None, is_business:
    bool = None, is_call_to_action_enabled: Union[bool, None] = None, nametag: dict = None, phone_number: str = None, pk: int = None,
                 professional_conversion_suggested_account_type: int = None, profile_pic_id: str = None, profile_pic_url: str = None,
                 show_insights_terms: bool = None, total_igtv_videos: int = None, username: str = None,
                 is_private: bool = None, is_verified: bool = None, reel_auto_archive: str = None, is_using_unified_inbox_for_direct:
            bool = None, can_hide_category: str = None, can_hide_public_contacts: str = None, *args, **kwargs):
        self.account_badges = account_badges
        self.account_type = account_type
        self.allow_contacts_sync = allow_contacts_sync
        self.allowed_commenter_type = allowed_commenter_type
        self.can_boost_post = can_boost_post
        self.can_see_organic_insights = can_see_organic_insights
        self.can_see_primary_country_in_settings = can_see_primary_country_in_settings
        self.full_name = full_name
        self.has_anonymous_profile_picture = has_anonymous_profile_picture
        self.has_placed_orders = has_placed_orders
        self.interop_messaging_user_fbid = interop_messaging_user_fbid
        self.is_business = is_business
        self.is_call_to_action_enabled = is_call_to_action_enabled
        self.nametag = nametag
        self.phone_number = phone_number
        self.pk = pk
        self.professional_conversion_suggested_account_type = professional_conversion_suggested_account_type
        self.profile_pic_id = profile_pic_id
        self.profile_pic_url = profile_pic_url
        self.show_insights_terms = show_insights_terms
        self.total_igtv_videos = total_igtv_videos
        self.username = username
        self.is_private = is_private
        self.is_verified = is_verified
        self.reel_auto_archive = reel_auto_archive
        self.is_using_unified_inbox_for_direct = is_using_unified_inbox_for_direct
        self.can_hide_category = can_hide_category
        self.can_hide_public_contacts = can_hide_public_contacts

    def __repr__(self):
        return pprint.pformat(vars(self))