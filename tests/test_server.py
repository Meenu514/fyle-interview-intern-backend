
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


