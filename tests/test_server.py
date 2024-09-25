import pytest
from core.libs.exceptions import FyleError

# Test the to_dict method of FyleError
def test_fyle_error_to_dict():
    error_message = "This is a test error"
    status_code = 500

    # Create FyleError instance
    error = FyleError(status_code=status_code, message=error_message)

    # Convert to dict
    error_dict = error.to_dict()

    # Assert the dictionary content
    assert isinstance(error_dict, dict)
    assert 'message' in error_dict
    assert error_dict['message'] == error_message


# Test raising the FyleError exception
def test_fyle_error_exception_handling():
    error_message = "Something went wrong"
    status_code = 400

    # Test raising the exception
    with pytest.raises(FyleError) as exc_info:
        raise FyleError(status_code=status_code, message=error_message)

    # Assert the exception details
    assert exc_info.value.status_code == status_code
    assert exc_info.value.message == error_message


# Test default status code if not provided (optional)
def test_fyle_error_default_status_code():
    error_message = "Default status code error"

    # Create FyleError instance without passing status_code
    error = FyleError(message=error_message, status_code=FyleError.status_code)

    # Assert the default status code is used
    assert error.status_code == 400
    assert error.message == error_message

def test_ready(client):
    response = client.get(
        '/',
    )

    assert response.status_code == 200


def test_no_api(client):
    response = client.get(
        '/hello',
    )   
    assert response.status_code == 404

def test_no_auth_header_error(client):
    for url in ['/student/assignments', '/teacher/assignments', '/principal/assignments']:
        response = client.get(
            url
        )

        assert response.status_code == 401

def test_incorrect_auth_token_error(client, h_student_1, h_teacher_1, h_principal):
    for url in ['/teacher/assignments', '/principal/assignments']:
        response = client.get(
            url,
            headers=h_student_1
        )

        assert response.status_code == 403

    for url in ['/student/assignments', '/principal/assignments']:
        response = client.get(
            url,
            headers=h_teacher_1
        )

        assert response.status_code == 403

    for url in ['/student/assignments', '/teacher/assignments']:
        response = client.get(
            url,
            headers=h_principal
        )

        assert response.status_code == 403


def test_role_specific_access(client, h_student_1, h_teacher_1, h_principal):
    # Student should access student assignments
    response = client.get(
        '/student/assignments',
        headers=h_student_1
    )
    assert response.status_code == 200

    # Teacher should access teacher assignments
    response = client.get(
        '/teacher/assignments',
        headers=h_teacher_1
    )
    assert response.status_code == 200

    # Principal should access principal assignments
    response = client.get(
        '/principal/assignments',
        headers=h_principal
    )
    assert response.status_code == 200

def test_fyle_error_exception_handling():
    error_message = "Something went wrong"
    status_code = 400

    # Test raising the exception
    with pytest.raises(FyleError) as exc_info:
        raise FyleError(status_code=status_code, message=error_message)

    # Assert the exception details
    assert exc_info.value.status_code == status_code
    assert exc_info.value.message == error_message
    
   # Test role access for invalid URLs
def test_role_access_invalid_urls(client, h_student_1, h_teacher_1, h_principal):
    invalid_urls = ['/invalid-url', '/another-invalid-url']
    
    for url in invalid_urls:
        response = client.get(url, headers=h_student_1)
        assert response.status_code == 404
        
        response = client.get(url, headers=h_teacher_1)
        assert response.status_code == 404
        
        response = client.get(url, headers=h_principal)
        assert response.status_code == 404 
    
