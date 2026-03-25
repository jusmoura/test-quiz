import pytest
from model import Question, Choice


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_remove_choice_by_id():
    q = Question(title='q1')
    c1 = q.add_choice('a')
    c2 = q.add_choice('b')

    q.remove_choice_by_id(c1.id)

    assert len(q.choices) == 1
    assert q.choices[0].id == c2.id


def test_remove_choice_invalid_id():
    q = Question(title='q1')
    q.add_choice('a')

    with pytest.raises(Exception):
        q.remove_choice_by_id(999)


def test_remove_all_choices():
    q = Question(title='q1')
    q.add_choice('a')
    q.add_choice('b')

    q.remove_all_choices()

    assert len(q.choices) == 0


def test_set_correct_choices():
    q = Question(title='q1')
    c1 = q.add_choice('a')
    c2 = q.add_choice('b')

    q.set_correct_choices([c2.id])

    assert not c1.is_correct
    assert c2.is_correct


def test_set_correct_choices_invalid_id():
    q = Question(title='q1')
    q.add_choice('a')

    with pytest.raises(Exception):
        q.set_correct_choices([999])


def test_correct_selected_choices():
    q = Question(title='q1', max_selections=2)
    c1 = q.add_choice('a')
    c2 = q.add_choice('b', True)

    result = q.correct_selected_choices([c1.id, c2.id])

    assert result == [c2.id]


def test_correct_selected_choices_exceeds_max():
    q = Question(title='q1', max_selections=1)
    c1 = q.add_choice('a')
    c2 = q.add_choice('b')

    with pytest.raises(Exception):
        q.correct_selected_choices([c1.id, c2.id])


def test_choice_text_validation():
    with pytest.raises(Exception):
        Choice(id=1, text='')


def test_choice_text_max_length():
    text = 'a' * 100
    c = Choice(id=1, text=text)

    assert c.text == text


def test_choice_text_too_long():
    with pytest.raises(Exception):
        Choice(id=1, text='a' * 101)
