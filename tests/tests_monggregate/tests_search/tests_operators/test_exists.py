from monggregate.search.operators.exists import Exists

def test_exists_expression():
    # Setup
    path = "email"

    exists_op = Exists(path=path)

    expected_expression = {
        "exists": {
            "path": path
        }
    }

    # Act
    actual_expression = exists_op.expression

    # Assert
    assert actual_expression == expected_expression