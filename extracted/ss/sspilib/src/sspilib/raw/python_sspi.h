#if defined(SSPILIB_IS_LINUX)
// We need to redefine all the relevant entries in the Windows headers
#include <stdint.h>

// Windows.h
typedef unsigned short WCHAR;
typedef WCHAR *LPWSTR;
typedef WCHAR SEC_WCHAR;
typedef void *PVOID;

typedef unsigned short USHORT;

// Ensure LONG matches up with the Win32 length
typedef int32_t LONG;
typedef uint32_t ULONG;

#define SEC_E_OK 0x00000000L
#define SEC_I_CONTINUE_NEEDED 0x00090312L
#define SEC_I_COMPLETE_NEEDED 0x00090313L
#define SEC_I_COMPLETE_AND_CONTINUE 0x00090314L

// guiddef.h
typedef struct _GUID
{
    unsigned long Data1;
    unsigned short Data2;
    unsigned short Data3;
    unsigned char Data4[8];
} GUID;

// sspi.h
#define SECPKG_ATTR_SIZES 0
#define SECPKG_ATTR_NAMES 1
#define SECPKG_ATTR_LIFESPAN 2
#define SECPKG_ATTR_DCE_INFO 3
#define SECPKG_ATTR_STREAM_SIZES 4
#define SECPKG_ATTR_KEY_INFO 5
#define SECPKG_ATTR_AUTHORITY 6
#define SECPKG_ATTR_PROTO_INFO 7
#define SECPKG_ATTR_PASSWORD_EXPIRY 8
#define SECPKG_ATTR_SESSION_KEY 9
#define SECPKG_ATTR_PACKAGE_INFO 10
#define SECPKG_ATTR_USER_FLAGS 11
#define SECPKG_ATTR_NEGOTIATION_INFO 12
#define SECPKG_ATTR_NATIVE_NAMES 13
#define SECPKG_ATTR_FLAGS 14
#define SECPKG_ATTR_USE_VALIDATED 15
#define SECPKG_ATTR_CREDENTIAL_NAME 16
#define SECPKG_ATTR_TARGET_INFORMATION 17
#define SECPKG_ATTR_ACCESS_TOKEN 18
#define SECPKG_ATTR_TARGET 19
#define SECPKG_ATTR_AUTHENTICATION_ID 20
#define SECPKG_ATTR_LOGOFF_TIME 21
#define SECPKG_ATTR_NEGO_KEYS 22
#define SECPKG_ATTR_PROMPTING_NEEDED 24
#define SECPKG_ATTR_UNIQUE_BINDINGS 25
#define SECPKG_ATTR_ENDPOINT_BINDINGS 26
#define SECPKG_ATTR_CLIENT_SPECIFIED_TARGET 27
#define SECPKG_ATTR_LAST_CLIENT_TOKEN_STATUS 30
#define SECPKG_ATTR_NEGO_PKG_INFO 31
#define SECPKG_ATTR_NEGO_STATUS 32
#define SECPKG_ATTR_CONTEXT_DELETED 33
#define SECPKG_ATTR_DTLS_MTU 34
#define SECPKG_ATTR_DATAGRAM_SIZES SECPKG_ATTR_STREAM_SIZES
#define SECPKG_ATTR_SUBJECT_SECURITY_ATTRIBUTES 128
#define SECPKG_ATTR_APPLICATION_PROTOCOL 35
#define SECPKG_ATTR_NEGOTIATED_TLS_EXTENSIONS 36
#define SECPKG_ATTR_IS_LOOPBACK 37

#define SECPKG_CRED_ATTR_NAMES 1
#define SECPKG_CRED_ATTR_SSI_PROVIDER 2
#define SECPKG_CRED_ATTR_KDC_PROXY_SETTINGS 3
#define SECPKG_CRED_ATTR_CERT 4
#define SECPKG_CRED_ATTR_PAC_BYPASS 5

#define KDC_PROXY_SETTINGS_V1 1
#define KDC_PROXY_SETTINGS_FLAGS_FORCEPROXY 0x1

#define SECURITY_NATIVE_DREP 0x00000010
#define SECURITY_NETWORK_DREP 0x00000000

#define SECPKG_CRED_INBOUND 0x00000001
#define SECPKG_CRED_OUTBOUND 0x00000002
#define SECPKG_CRED_BOTH 0x00000003
#define SECPKG_CRED_DEFAULT 0x00000004
#define SECPKG_CRED_RESERVED 0xF0000000
#define SECPKG_CRED_AUTOLOGON_RESTRICTED 0x00000010
#define SECPKG_CRED_PROCESS_POLICY_ONLY 0x00000020

#define SEC_WINNT_AUTH_IDENTITY_ANSI 0x1
#define SEC_WINNT_AUTH_IDENTITY_UNICODE 0x2
#define SEC_WINNT_AUTH_IDENTITY_MARSHALLED 0x4
#define SEC_WINNT_AUTH_IDENTITY_ONLY 0x8
#define SEC_WINNT_AUTH_IDENTITY_FLAGS_PROCESS_ENCRYPTED 0x10
#define SEC_WINNT_AUTH_IDENTITY_FLAGS_SYSTEM_PROTECTED 0x20
#define SEC_WINNT_AUTH_IDENTITY_FLAGS_USER_PROTECTED 0x40
#define SEC_WINNT_AUTH_IDENTITY_FLAGS_SYSTEM_ENCRYPTED 0x80
#define SEC_WINNT_AUTH_IDENTITY_FLAGS_RESERVED 0x10000
#define SEC_WINNT_AUTH_IDENTITY_FLAGS_NULL_USER 0x20000
#define SEC_WINNT_AUTH_IDENTITY_FLAGS_NULL_DOMAIN 0x40000
#define SEC_WINNT_AUTH_IDENTITY_FLAGS_ID_PROVIDER 0x80000
#define SEC_WINNT_AUTH_IDENTITY_VERSION 0x200
#define SEC_WINNT_AUTH_IDENTITY_VERSION_2 0x201

#define SECQOP_WRAP_NO_ENCRYPT 0x80000001
#define SECQOP_WRAP_OOB_DATA 0x40000000

#define SECBUFFER_VERSION 0

#define SECBUFFER_EMPTY 0
#define SECBUFFER_DATA 1
#define SECBUFFER_TOKEN 2
#define SECBUFFER_PKG_PARAMS 3
#define SECBUFFER_MISSING 4
#define SECBUFFER_EXTRA 5
#define SECBUFFER_STREAM_TRAILER 6
#define SECBUFFER_STREAM_HEADER 7
#define SECBUFFER_NEGOTIATION_INFO 8
#define SECBUFFER_PADDING 9
#define SECBUFFER_STREAM 10
#define SECBUFFER_MECHLIST 11
#define SECBUFFER_MECHLIST_SIGNATURE 12
#define SECBUFFER_TARGET 13
#define SECBUFFER_CHANNEL_BINDINGS 14
#define SECBUFFER_CHANGE_PASS_RESPONSE 15
#define SECBUFFER_TARGET_HOST 16
#define SECBUFFER_ALERT 17
#define SECBUFFER_APPLICATION_PROTOCOLS 18
#define SECBUFFER_SRTP_PROTECTION_PROFILES 19
#define SECBUFFER_SRTP_MASTER_KEY_IDENTIFIER 20
#define SECBUFFER_TOKEN_BINDING 21
#define SECBUFFER_PRESHARED_KEY 22
#define SECBUFFER_PRESHARED_KEY_IDENTITY 23
#define SECBUFFER_DTLS_MTU 24
#define SECBUFFER_SEND_GENERIC_TLS_EXTENSION 25
#define SECBUFFER_SUBSCRIBE_GENERIC_TLS_EXTENSION 26
#define SECBUFFER_FLAGS 27
#define SECBUFFER_TRAFFIC_SECRETS 28
#define SECBUFFER_CERTIFICATE_REQUEST_CONTEXT 29

#define SECBUFFER_ATTRMASK 0xF0000000
#define SECBUFFER_READONLY 0x80000000
#define SECBUFFER_READONLY_WITH_CHECKSUM 0x10000000
#define SECBUFFER_RESERVED 0x60000000

#define ISC_REQ_DELEGATE 0x00000001
#define ISC_REQ_MUTUAL_AUTH 0x00000002
#define ISC_REQ_REPLAY_DETECT 0x00000004
#define ISC_REQ_SEQUENCE_DETECT 0x00000008
#define ISC_REQ_CONFIDENTIALITY 0x00000010
#define ISC_REQ_USE_SESSION_KEY 0x00000020
#define ISC_REQ_PROMPT_FOR_CREDS 0x00000040
#define ISC_REQ_USE_SUPPLIED_CREDS 0x00000080
#define ISC_REQ_ALLOCATE_MEMORY 0x00000100
#define ISC_REQ_USE_DCE_STYLE 0x00000200
#define ISC_REQ_DATAGRAM 0x00000400
#define ISC_REQ_CONNECTION 0x00000800
#define ISC_REQ_CALL_LEVEL 0x00001000
#define ISC_REQ_FRAGMENT_SUPPLIED 0x00002000
#define ISC_REQ_EXTENDED_ERROR 0x00004000
#define ISC_REQ_STREAM 0x00008000
#define ISC_REQ_INTEGRITY 0x00010000
#define ISC_REQ_IDENTIFY 0x00020000
#define ISC_REQ_NULL_SESSION 0x00040000
#define ISC_REQ_MANUAL_CRED_VALIDATION 0x00080000
#define ISC_REQ_RESERVED1 0x00100000
#define ISC_REQ_FRAGMENT_TO_FIT 0x00200000
#define ISC_REQ_FORWARD_CREDENTIALS 0x00400000
#define ISC_REQ_NO_INTEGRITY 0x00800000
#define ISC_REQ_USE_HTTP_STYLE 0x01000000
#define ISC_REQ_UNVERIFIED_TARGET_NAME 0x20000000
#define ISC_REQ_CONFIDENTIALITY_ONLY 0x40000000

#define ISC_RET_DELEGATE 0x00000001
#define ISC_RET_MUTUAL_AUTH 0x00000002
#define ISC_RET_REPLAY_DETECT 0x00000004
#define ISC_RET_SEQUENCE_DETECT 0x00000008
#define ISC_RET_CONFIDENTIALITY 0x00000010
#define ISC_RET_USE_SESSION_KEY 0x00000020
#define ISC_RET_USED_COLLECTED_CREDS 0x00000040
#define ISC_RET_USED_SUPPLIED_CREDS 0x00000080
#define ISC_RET_ALLOCATED_MEMORY 0x00000100
#define ISC_RET_USED_DCE_STYLE 0x00000200
#define ISC_RET_DATAGRAM 0x00000400
#define ISC_RET_CONNECTION 0x00000800
#define ISC_RET_INTERMEDIATE_RETURN 0x00001000
#define ISC_RET_CALL_LEVEL 0x00002000
#define ISC_RET_EXTENDED_ERROR 0x00004000
#define ISC_RET_STREAM 0x00008000
#define ISC_RET_INTEGRITY 0x00010000
#define ISC_RET_IDENTIFY 0x00020000
#define ISC_RET_NULL_SESSION 0x00040000
#define ISC_RET_MANUAL_CRED_VALIDATION 0x00080000
#define ISC_RET_RESERVED1 0x00100000
#define ISC_RET_FRAGMENT_ONLY 0x00200000
#define ISC_RET_FORWARD_CREDENTIALS 0x00400000
#define ISC_RET_USED_HTTP_STYLE 0x01000000
#define ISC_RET_NO_ADDITIONAL_TOKEN 0x02000000
#define ISC_RET_REAUTHENTICATION 0x08000000
#define ISC_RET_CONFIDENTIALITY_ONLY 0x40000000

#define ASC_REQ_DELEGATE 0x00000001
#define ASC_REQ_MUTUAL_AUTH 0x00000002
#define ASC_REQ_REPLAY_DETECT 0x00000004
#define ASC_REQ_SEQUENCE_DETECT 0x00000008
#define ASC_REQ_CONFIDENTIALITY 0x00000010
#define ASC_REQ_USE_SESSION_KEY 0x00000020
#define ASC_REQ_SESSION_TICKET 0x00000040
#define ASC_REQ_ALLOCATE_MEMORY 0x00000100
#define ASC_REQ_USE_DCE_STYLE 0x00000200
#define ASC_REQ_DATAGRAM 0x00000400
#define ASC_REQ_CONNECTION 0x00000800
#define ASC_REQ_CALL_LEVEL 0x00001000
#define ASC_REQ_FRAGMENT_SUPPLIED 0x00002000
#define ASC_REQ_EXTENDED_ERROR 0x00008000
#define ASC_REQ_STREAM 0x00010000
#define ASC_REQ_INTEGRITY 0x00020000
#define ASC_REQ_LICENSING 0x00040000
#define ASC_REQ_IDENTIFY 0x00080000
#define ASC_REQ_ALLOW_NULL_SESSION 0x00100000
#define ASC_REQ_ALLOW_NON_USER_LOGONS 0x00200000
#define ASC_REQ_ALLOW_CONTEXT_REPLAY 0x00400000
#define ASC_REQ_FRAGMENT_TO_FIT 0x00800000
#define ASC_REQ_NO_TOKEN 0x01000000
#define ASC_REQ_PROXY_BINDINGS 0x04000000
#define ASC_REQ_ALLOW_MISSING_BINDINGS 0x10000000

#define ASC_RET_DELEGATE 0x00000001
#define ASC_RET_MUTUAL_AUTH 0x00000002
#define ASC_RET_REPLAY_DETECT 0x00000004
#define ASC_RET_SEQUENCE_DETECT 0x00000008
#define ASC_RET_CONFIDENTIALITY 0x00000010
#define ASC_RET_USE_SESSION_KEY 0x00000020
#define ASC_RET_SESSION_TICKET 0x00000040
#define ASC_RET_ALLOCATED_MEMORY 0x00000100
#define ASC_RET_USED_DCE_STYLE 0x00000200
#define ASC_RET_DATAGRAM 0x00000400
#define ASC_RET_CONNECTION 0x00000800
#define ASC_RET_CALL_LEVEL 0x00002000
#define ASC_RET_THIRD_LEG_FAILED 0x00004000
#define ASC_RET_EXTENDED_ERROR 0x00008000
#define ASC_RET_STREAM 0x00010000
#define ASC_RET_INTEGRITY 0x00020000
#define ASC_RET_LICENSING 0x00040000
#define ASC_RET_IDENTIFY 0x00080000
#define ASC_RET_NULL_SESSION 0x00100000
#define ASC_RET_ALLOW_NON_USER_LOGONS 0x00200000
#define ASC_RET_ALLOW_CONTEXT_REPLAY 0x00400000
#define ASC_RET_FRAGMENT_ONLY 0x00800000
#define ASC_RET_NO_TOKEN 0x01000000
#define ASC_RET_NO_ADDITIONAL_TOKEN 0x02000000

#define SECPKG_FLAG_INTEGRITY 0x00000001
#define SECPKG_FLAG_PRIVACY 0x00000002
#define SECPKG_FLAG_TOKEN_ONLY 0x00000004
#define SECPKG_FLAG_DATAGRAM 0x00000008
#define SECPKG_FLAG_CONNECTION 0x00000010
#define SECPKG_FLAG_MULTI_REQUIRED 0x00000020
#define SECPKG_FLAG_CLIENT_ONLY 0x00000040
#define SECPKG_FLAG_EXTENDED_ERROR 0x00000080
#define SECPKG_FLAG_IMPERSONATION 0x00000100
#define SECPKG_FLAG_ACCEPT_WIN32_NAME 0x00000200
#define SECPKG_FLAG_STREAM 0x00000400
#define SECPKG_FLAG_NEGOTIABLE 0x00000800
#define SECPKG_FLAG_GSS_COMPATIBLE 0x00001000
#define SECPKG_FLAG_LOGON 0x00002000
#define SECPKG_FLAG_ASCII_BUFFERS 0x00004000
#define SECPKG_FLAG_FRAGMENT 0x00008000
#define SECPKG_FLAG_MUTUAL_AUTH 0x00010000
#define SECPKG_FLAG_DELEGATION 0x00020000
#define SECPKG_FLAG_READONLY_WITH_CHECKSUM 0x00040000
#define SECPKG_FLAG_RESTRICTED_TOKENS 0x00080000
#define SECPKG_FLAG_NEGO_EXTENDER 0x00100000
#define SECPKG_FLAG_NEGOTIABLE2 0x00200000
#define SECPKG_FLAG_APPCONTAINER_PASSTHROUGH 0x00400000
#define SECPKG_FLAG_APPCONTAINER_CHECKS 0x00800000
#define SECPKG_FLAG_CREDENTIAL_ISOLATION_ENABLED 0x01000000
#define SECPKG_FLAG_APPLY_LOOPBACK 0x02000000

// {28BFC32F-10F6-4738-98D1-1AC061DF716A}
const GUID SEC_WINNT_AUTH_DATA_TYPE_PASSWORD =
    {0x28bfc32f, 0x10f6, 0x4738, {0x98, 0xd1, 0x1a, 0xc0, 0x61, 0xdf, 0x71, 0x6a}};

// {235F69AD-73FB-4dbc-8203-0629E739339B}
const GUID SEC_WINNT_AUTH_DATA_TYPE_CERT =
    {0x235f69ad, 0x73fb, 0x4dbc, {0x82, 0x3, 0x6, 0x29, 0xe7, 0x39, 0x33, 0x9b}};

// {7CB72412-1016-491A-8C87-4D2AA1B7DD3A}
const GUID SEC_WINNT_AUTH_DATA_TYPE_CREDMAN_CERT =
    {0x7cb72412, 0x1016, 0x491a, {0x8c, 0x87, 0x4d, 0x2a, 0xa1, 0xb7, 0xdd, 0x3a}};

// {10A47879-5EBF-4B85-BD8D-C21BB4F49C8A}
const GUID SEC_WINNT_AUTH_DATA_TYPE_NGC =
    {0x10a47879, 0x5ebf, 0x4b85, {0xbd, 0x8d, 0xc2, 0x1b, 0xb4, 0xf4, 0x9c, 0x8a}};

// {32E8F8D7-7871-4BCC-83C5-460F66C6135C}
const GUID SEC_WINNT_AUTH_DATA_TYPE_FIDO =
    {0x32e8f8d7, 0x7871, 0x4bcc, {0x83, 0xc5, 0x46, 0xf, 0x66, 0xc6, 0x13, 0x5c}};

// {D587AAE8-F78F-4455-A112-C934BEEE7CE1}
const GUID SEC_WINNT_AUTH_DATA_TYPE_KEYTAB =
    {0xd587aae8, 0xf78f, 0x4455, {0xa1, 0x12, 0xc9, 0x34, 0xbe, 0xee, 0x7c, 0xe1}};

// {12E52E0F-6F9B-4F83-9020-9DE42B226267}
const GUID SEC_WINNT_AUTH_DATA_TYPE_DELEGATION_TOKEN =
    {0x12e52e0f, 0x6f9b, 0x4f83, {0x90, 0x20, 0x9d, 0xe4, 0x2b, 0x22, 0x62, 0x67}};

// {68FD9879-079C-4dfe-8281-578AADC1C100}
const GUID SEC_WINNT_AUTH_DATA_TYPE_CSP_DATA =
    {0x68fd9879, 0x79c, 0x4dfe, {0x82, 0x81, 0x57, 0x8a, 0xad, 0xc1, 0xc1, 0x0}};

// {B86C4FF3-49D7-4DC4-B560-B1163685B236}
const GUID SEC_WINNT_AUTH_DATA_TYPE_SMARTCARD_CONTEXTS =
    {0xb86c4ff3, 0x49d7, 0x4dc4, {0xb5, 0x60, 0xb1, 0x16, 0x36, 0x85, 0xb2, 0x36}};

typedef LONG SECURITY_STATUS;
typedef uintptr_t ULONG_PTR;

typedef struct _SecPkgInfoW
{
    ULONG fCapabilities;
    unsigned short wVersion;
    unsigned short wRPCID;
    ULONG cbMaxToken;
    LPWSTR Name;
    LPWSTR Comment;
} SecPkgInfoW, *PSecPkgInfoW;

typedef struct _SECURITY_INTEGER
{
    ULONG LowPart;
    LONG HighPart;
} SECURITY_INTEGER, *PSECURITY_INTEGER;
typedef SECURITY_INTEGER TimeStamp;
typedef SECURITY_INTEGER *PTimeStamp;

typedef struct _SecHandle
{
    ULONG_PTR dwLower;
    ULONG_PTR dwUpper;
} SecHandle, *PSecHandle;

typedef SecHandle CredHandle;
typedef PSecHandle PCredHandle;

typedef SecHandle CtxtHandle;
typedef PSecHandle PCtxtHandle;

typedef struct _SecPkgContext_NamesW
{
    SEC_WCHAR *sUserName;
} SecPkgContext_NamesW, *PSecPkgContext_NamesW;

typedef struct _SecPkgContext_PackageInfoW
{
    PSecPkgInfoW PackageInfo;
} SecPkgContext_PackageInfoW, *PSecPkgContext_PackageInfoW;

typedef struct _SecPkgContext_Sizes
{
    ULONG cbMaxToken;
    ULONG cbMaxSignature;
    ULONG cbBlockSize;
    ULONG cbSecurityTrailer;
} SecPkgContext_Sizes, *PSecPkgContext_Sizes;

typedef struct _SecPkgContext_SessionKey
{
    ULONG SessionKeyLength;
    unsigned char *SessionKey;
} SecPkgContext_SessionKey, *PSecPkgContext_SessionKey;

typedef struct _SecPkgCredentials_KdcProxySettingsW
{
    ULONG Version;
    ULONG Flags;
    USHORT ProxyServerOffset;
    USHORT ProxyServerLength;
    USHORT ClientTlsCredOffset;
    USHORT ClientTlsCredLength;
} SecPkgCredentials_KdcProxySettingsW, *PSecPkgCredentials_KdcProxySettingsW;

typedef struct _SEC_WINNT_AUTH_IDENTITY_EXW
{
    ULONG Version;
    ULONG Length;
    unsigned short *User;
    ULONG UserLength;
    unsigned short *Domain;
    ULONG DomainLength;
    unsigned short *Password;
    ULONG PasswordLength;
    ULONG Flags;
    unsigned short *PackageList;
    ULONG PackageListLength;
} SEC_WINNT_AUTH_IDENTITY_EXW, *PSEC_WINNT_AUTH_IDENTITY_EXW;

typedef struct _SEC_WINNT_AUTH_IDENTITY_EX2
{
    ULONG Version;
    unsigned short cbHeaderLength;
    ULONG cbStructureLength;
    ULONG UserOffset;
    unsigned short UserLength;
    ULONG DomainOffset;
    unsigned short DomainLength;
    ULONG PackedCredentialsOffset;
    unsigned short PackedCredentialsLength;
    ULONG Flags;
    ULONG PackageListOffset;
    ULONG PackageListLength;
} SEC_WINNT_AUTH_IDENTITY_EX2, *PSEC_WINNT_AUTH_IDENTITY_EX2;

typedef struct _SEC_WINNT_AUTH_BYTE_VECTOR
{
    unsigned long ByteArrayOffset;
    unsigned short ByteArrayLength;
} SEC_WINNT_AUTH_BYTE_VECTOR, *PSEC_WINNT_AUTH_BYTE_VECTOR;

typedef struct _SEC_WINNT_AUTH_DATA
{
    GUID CredType;
    SEC_WINNT_AUTH_BYTE_VECTOR CredData;
} SEC_WINNT_AUTH_DATA, *PSEC_WINNT_AUTH_DATA;

typedef struct _SEC_WINNT_AUTH_PACKED_CREDENTIALS
{
    unsigned short cbHeaderLength;
    unsigned short cbStructureLength;
    SEC_WINNT_AUTH_DATA AuthData;
} SEC_WINNT_AUTH_PACKED_CREDENTIALS, *PSEC_WINNT_AUTH_PACKED_CREDENTIALS;

typedef struct _SecBuffer
{
    ULONG cbBuffer;
    ULONG BufferType;
    void *pvBuffer;
} SecBuffer, *PSecBuffer;

typedef struct _SecBufferDesc
{
    ULONG ulVersion;
    ULONG cBuffers;
    PSecBuffer pBuffers;
} SecBufferDesc, *PSecBufferDesc;

typedef struct _SEC_CHANNEL_BINDINGS
{
    ULONG dwInitiatorAddrType;
    ULONG cbInitiatorLength;
    ULONG dwInitiatorOffset;
    ULONG dwAcceptorAddrType;
    ULONG cbAcceptorLength;
    ULONG dwAcceptorOffset;
    ULONG cbApplicationDataLength;
    ULONG dwApplicationDataOffset;
} SEC_CHANNEL_BINDINGS, *PSEC_CHANNEL_BINDINGS;

typedef void (*SEC_GET_KEY_FN)(
    void *Arg,              // Argument passed in
    void *Principal,        // Principal ID
    ULONG KeyVer,           // Key Version
    void **Key,             // Returned ptr to key
    SECURITY_STATUS *Status // returned status
);

SECURITY_STATUS
AcquireCredentialsHandleW(
    LPWSTR pszPrincipal,
    LPWSTR pszPackage,
    ULONG fCredentialUse,
    void *pvLogonId,
    void *pAuthData,
    SEC_GET_KEY_FN pGetKeyFn,
    void *pvGetKeyArgument,
    PCredHandle phCredential,
    PTimeStamp ptsExpiry);

SECURITY_STATUS
AcceptSecurityContext(
    PCredHandle phCredential,
    PCtxtHandle phContext,
    PSecBufferDesc pInput,
    ULONG fContextReq,
    ULONG TargetDataRep,
    PCtxtHandle phNewContext,
    PSecBufferDesc pOutput,
    ULONG *pfContextAttr,
    PTimeStamp ptsExpiry);

SECURITY_STATUS
CompleteAuthToken(
    PCtxtHandle phContext,
    PSecBufferDesc pToken);

SECURITY_STATUS
DecryptMessage(PCtxtHandle phContext,
               PSecBufferDesc pMessage,
               ULONG MessageSeqNo,
               ULONG *pfQOP);

SECURITY_STATUS
DeleteSecurityContext(
    PCtxtHandle phContext);

SECURITY_STATUS
EncryptMessage(PCtxtHandle phContext,
               ULONG fQOP,
               PSecBufferDesc pMessage,
               ULONG MessageSeqNo);

SECURITY_STATUS
EnumerateSecurityPackagesW(
    ULONG *pcPackages,
    PSecPkgInfoW *ppPackageInfo);

SECURITY_STATUS
FreeContextBuffer(
    PVOID pvContextBuffer);

SECURITY_STATUS
FreeCredentialsHandle(
    PCredHandle phCredential);

SECURITY_STATUS
InitializeSecurityContextW(
    PCredHandle phCredential,
    PCtxtHandle phContext,
    LPWSTR pszTargetName,
    ULONG fContextReq,
    ULONG Reserved1,
    ULONG TargetDataRep,
    PSecBufferDesc pInput,
    ULONG Reserved2,
    PCtxtHandle phNewContext,
    PSecBufferDesc pOutput,
    ULONG *pfContextAttr,
    PTimeStamp ptsExpiry);

SECURITY_STATUS
MakeSignature(
    PCtxtHandle phContext,
    ULONG fQOP,
    PSecBufferDesc pMessage,
    ULONG MessageSeqNo);

SECURITY_STATUS
QueryContextAttributesW(
    PCtxtHandle phContext,
    ULONG ulAttribute,
    void *pBuffer);

SECURITY_STATUS
SetCredentialsAttributesW(
    PCredHandle phCredential,
    ULONG ulAttribute,
    void *pBuffer,
    ULONG cbBuffer);

SECURITY_STATUS
VerifySignature(
    PCtxtHandle phContext,
    PSecBufferDesc pMessage,
    ULONG MessageSeqNo,
    ULONG *pfQOP);

// NTSecAPI.h
#define KERB_WRAP_NO_ENCRYPT 0x80000001

#else
// For Windows we just need to include the headers needed
#include <Windows.h>
#include <NTSecAPI.h>
#include <security.h>

#endif
