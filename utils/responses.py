from rest_framework import status


class ErrorCollection(object):
    def __init__(self, response_code, status_code, message):
        self.response_code = response_code
        self.status_code = status_code
        self.message = message

    def as_md(self):
        return '\n\n> **%s**\n\n```\n{\n\n\t"code": "%s"\n\n\t"message": "%s"\n\n}\n\n```' % \
               (self.message, self.status_code, self.message)


class OAuthErrorCollection(object):
    OAUTH_401_PROVIDER_INVALID = ErrorCollection(
        response_code='OAUTH_401_PROVIDER_INVALID',
        status_code=status.HTTP_401_UNAUTHORIZED,
        message='올바르지 못한 OAuth Provider 정보입니다.'
    )

    OAUTH_401_ID_TOKEN_INVALID = ErrorCollection(
        response_code='OAUTH_401_ID_TOKEN_INVALID',
        status_code=status.HTTP_401_UNAUTHORIZED,
        message='올바르지 못한 OAuth id_token 정보입니다.'
    )

    OAUTH_403_USER_ALREADY_EXISTS = ErrorCollection(
        response_code='OAUTH_403_USER_ALREADY_EXISTS',
        status_code=status.HTTP_403_FORBIDDEN,
        message='이미 존재하는 OAuth 사용자입니다.'
    )


class UserErrorCollection(object):
    USER_400_LOGIN_REQUEST_INVALID = ErrorCollection(
        response_code='USER_400_LOGIN_REQUEST_INVALID',
        status_code=status.HTTP_400_BAD_REQUEST,
        message='올바르지 못한 로그인 요청입니다(Invalid Login Credentials).'
    )

    USER_400_SIGNUP_REQUEST_INVALID = ErrorCollection(
        response_code='USER_400_REQUEST_INVALID',
        status_code=status.HTTP_400_BAD_REQUEST,
        message='올바르지 못한 회원가입 정보입니다.'
    )

    USER_400_INVALID_USER_TYPE_ERROR = ErrorCollection(
        response_code='USER_400_INVALID_USER_TYPE_ERROR',
        status_code=status.HTTP_400_BAD_REQUEST,
        message='프로필을 조회할 수 있는 올바른 타입의 유저(코치/트레이니)가 아닙니다.'
    )

    USER_404_PROFILE_ATTRIBUTE_ERROR = ErrorCollection(
        response_code='USER_404_PROFILE_ATTRIBUTE_ERROR',
        status_code=status.HTTP_404_NOT_FOUND,
        message='사용자 타입에 따른 세부 프로필에 접근하는 과정에서 오류가 발생했습니다.'
    )

    USER_404_PROFILE_DOES_NOT_EXISTS = ErrorCollection(
        response_code='USER_404_PROFILE_DOES_NOT_EXISTS',
        status_code=status.HTTP_404_NOT_FOUND,
        message='사용자 프로필이 존재하지 않습니다.'
    )

    USER_404_TRAINEE_PROFILE_DOES_NOT_EXISTS = ErrorCollection(
        response_code='USER_404_TRAINEE_PROFILE_DOES_NOT_EXISTS',
        status_code=status.HTTP_404_NOT_FOUND,
        message='트레이니 프로필이 존재하지 않습니다.'
    )

    USER_404_COACH_PROFILE_DOES_NOT_EXISTS = ErrorCollection(
        response_code='USER_404_COACH_PROFILE_DOES_NOT_EXISTS',
        status_code=status.HTTP_404_NOT_FOUND,
        message='코치 프로필이 존재하지 않습니다.'
    )

    USER_400_PROFILE_UPDATE_INVALID_USER_ERROR = ErrorCollection(
        response_code='USER_400_PROFILE_UPDATE_INVALID_USER_ERROR',
        status_code=status.HTTP_400_BAD_REQUEST,
        message='다른 유저 객체의 프로필을 수정할 수 없습니다.'
    )

    USER_404_PROFILE_UPDATE_INVALID_DATA_ERROR = ErrorCollection(
        response_code='USER_404_PROFILE_UPDATE_INVALID_DATA_ERROR',
        status_code=status.HTTP_400_BAD_REQUEST,
        message='입력받은 정보로 프로필을 업데이트 할 수 없습니다.'
    )

    USER_204_COACH_LIST_DOES_NOT_EXISTS = ErrorCollection(
        response_code='PROGRAM_204_COACH_LIST_DOES_NOT_EXISTS',
        status_code=status.HTTP_204_NO_CONTENT,
        message='서비스 내에 등록된 코치가 존재하지 않습니다.'
    )

    USER_404_COACH_LIST_SEARCH_VALUE_ERROR = ErrorCollection(
        response_code='PROGRAM_404_COACH_LIST_SEARCH_VALUE_ERROR',
        status_code=status.HTTP_404_NOT_FOUND,
        message='잘못된 코치 검색 옵션입니다.'
    )


class ProgramErrorCollection(object):
    PROGRAM_404_TRAINEE_PROFILE_DOES_NOT_EXISTS = ErrorCollection(
        response_code='PROGRAM_404_TRAINEE_DOES_NOT_EXISTS',
        status_code=status.HTTP_404_NOT_FOUND,
        message='트레이니 프로필이 존재하지 않습니다.'
    )

    PROGRAM_404_COACH_PROFILE_DOES_NOT_EXISTS = ErrorCollection(
        response_code='PROGRAM_404_COACH_PROFILE_DOES_NOT_EXISTS',
        status_code=status.HTTP_404_NOT_FOUND,
        message='코치 프로필이 존재하지 않습니다.'
    )

    PROGRAM_404_PROGRAM_SET_ATTRIBUTE_ERROR = ErrorCollection(
        response_code='PROGRAM_404_PROGRAM_SET_ATTRIBUTE_ERROR',
        status_code=status.HTTP_404_NOT_FOUND,
        message='트레이너가 등록한 프로그램이 존재하지 않습니다.'
    )

    PROGRAM_404_TRAINEE_ATTRIBUTE_ERROR = ErrorCollection(
        response_code='PROGRAM_404_TRAINEE_ATTRIBUTE_ERROR',
        status_code=status.HTTP_404_NOT_FOUND,
        message='프로그램 객체에 트레이니 정보가 존재하지 않습니다.'
    )

    PROGRAM_404_COACH_ATTRIBUTE_ERROR = ErrorCollection(
        response_code= 'PROGRAM_404_COACH_ATTRIBUTE_ERROR',
        status_code=status.HTTP_404_NOT_FOUND,
        message='프로그램 객체에 코치 정보가 존재하지 않습니다.'
    )

    PROGRAM_404_GOAL_ATTRIBUTE_ERROR = ErrorCollection(
        response_code='PROGRAM_404_COACH_ATTRIBUTE_ERROR',
        status_code=status.HTTP_404_NOT_FOUND,
        message='프로그램 객체에 목표 정보가 존재하지 않습니다.'
    )

    PROGRAM_404_QUEST_SET_ATTRIBUTE_ERROR = ErrorCollection(
        response_code='PROGRAM_404_QUEST_SET_ATTRIBUTE_ERROR',
        status_code=status.HTTP_404_NOT_FOUND,
        message='프로그램 객체에 퀘스트가 존재하지 않습니다.'
    )

    PROGRAM_400_CACHE_DOES_NOT_EXISTS = ErrorCollection(
        response_code='PROGRAM_400_CACHE_DOES_NOT_EXISTS',
        status_code=status.HTTP_400_BAD_REQUEST,
        message='요청을 처리할 캐시가 존재하지 않습니다.'
    )

    PROGRAM_400_NEW_COACH_REQUEST_DUPLICATE_ERROR = ErrorCollection(
        response_code='PROGRAM_400_NEW_COACH_REQUEST_DUPLICATE_ERROR',
        status_code=status.HTTP_400_BAD_REQUEST,
        message='이미 전송된 코치 등록 요청입니다.'
    )

    PROGRAM_400_COACH_REQUEST_DOES_NOT_EXISTS = ErrorCollection(
        response_code='PROGRAM_400_COACH_REQUEST_DOES_NOT_EXISTS',
        status_code=status.HTTP_404_NOT_FOUND,
        message='코치 등록 요청이 존재하지 않습니다.'
    )


class VerifyErrorCollection(object):
    VERIFY_400_NICKNAME_DUPLICATE_CHECK_VALIDATION_ERROR = ErrorCollection(
        response_code='VERIFY_400_NICKNAME_DUPLICATE_CHECK_VALIDATION_ERROR',
        status_code=status.HTTP_400_BAD_REQUEST,
        message='중복된 데이터입니다.'
    )

    VERIFY_400_NICKNAME_DUPLICATE_CHECK_PARAMETER_ERROR = ErrorCollection(
        response_code='USER_400_NICKNAME_DUPLICATE_CHECK_PARAMETER_ERROR',
        status_code=status.HTTP_400_BAD_REQUEST,
        message='중복 확인을 수행할 data parameter가 전달되지 않았습니다.'
    )

    VERIFY_400_COACHCODE_EXIST_CHECK_VALIDATION_ERROR = ErrorCollection(
        response_code='VERIFY_400_COACHCODE_EXIST_CHECK_VALIDATION_ERROR',
        status_code=status.HTTP_400_BAD_REQUEST,
        message='존재하지 않는 데이터입니다.'
    )

    VERIFY_400_COACHCODE_EXIST_CHECK_PARAMETER_ERROR = ErrorCollection(
        response_code='VERIFY_400_COACHCODE_EXIST_CHECK_PARAMETER_ERROR',
        status_code=status.HTTP_400_BAD_REQUEST,
        message='인증을 수행할 코치 코드가 data parameter로 전달되지 않았습니다.'
    )
