from monggregate.search.operators.more_like_this import MoreLikeThis

def test_more_like_this_expression():
    # Setup
    like_docs = [{"title": "Introduction to MongoDB"}, {"title": "Advanced MongoDB Usage"}]

    more_like_this = MoreLikeThis(like=like_docs)

    expected_expression = {
        "moreLikeThis": {
            "like": like_docs
        }
    }

    # Act
    actual_expression = more_like_this.expression

    # Assert
    assert actual_expression == expected_expression