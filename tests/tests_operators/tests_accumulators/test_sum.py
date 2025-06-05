def test_sum_operand():
    # Setup
    operand = "$amount"
    
    #Act
    result_op = {"$sum": operand}
    expected_expression = {"$sum": "$amount"}
    
    #Assert
    assert result_op == expected_expression