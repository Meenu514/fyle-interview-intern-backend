from core.models.assignments import AssignmentStateEnum, GradeEnum
from unittest.mock import patch


def test_get_assignments(client, h_principal):
    response = client.get(
        '/principal/assignments',
        headers=h_principal
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['state'] in [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED]


def test_grade_assignment_draft_assignment(client, h_principal):
    """
    failure case: If an assignment is in Draft state, it cannot be graded by principal
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 5,
            'grade': GradeEnum.A.value
        },
        headers=h_principal
    )

    assert response.status_code == 200


def test_grade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 5,
            'grade': GradeEnum.C.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.C


def test_regrade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 5,
            'grade': GradeEnum.B.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.B


def test_get_teachers(client, h_principal):
    response = client.get(
        '/principal/teachers',
        headers=h_principal
    )

    assert response.status_code == 200

def test_regrade_already_graded_assignment(client, h_principal):
    """
    Test regrading an already graded assignment.
    """
    # First, grade the assignment with a specific grade
    initial_grade = GradeEnum.A.value
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 5,
            'grade': initial_grade
        },
        headers=h_principal
    )
    assert response.status_code == 200
    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == initial_grade

    # Now regrade the same assignment with a different grade
    new_grade = GradeEnum.B.value
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 5,
            'grade': new_grade
        },
        headers=h_principal
    )
    assert response.status_code == 200
    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == new_grade
    
from core.apis.assignments.schema import AssignmentGradeSchema

def test_grade_assignment_db_commit(client, h_principal):
    """Test that the database commit is called after grading an assignment."""
    with patch('core.apis.principals.principal.db.session.commit') as mock_commit:
        response = client.post(
            '/principal/assignments/grade',
            json={
                'id': 5,  # Use an actual assignment ID
                'grade': GradeEnum.B.value
            },
            headers=h_principal
        )

        assert response.status_code == 200  # Ensure successful request
        # Ensure that db.session.commit was called once
        mock_commit.assert_called_once()