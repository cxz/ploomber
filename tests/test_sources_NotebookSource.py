import pytest

from ploomber.sources.NotebookSource import check_notebook_source

notebook_ab = """
# + tags=['parameters']
a = 1
b = 2

# +
a + b
"""


def test_error_if_parameters_cell_doesnt_exist():
    notebook_no_parameters_tag = """
    a + b
    """

    with pytest.raises(ValueError) as excinfo:
        check_notebook_source(notebook_no_parameters_tag, {'a': 1, 'b': 2})

    assert ('Notebook does not have a cell tagged "parameters"'
            == str(excinfo.value))


def test_returns_true_if_parameters_match():
    assert check_notebook_source(notebook_ab, {'a': 1, 'b': 2})


def test_warn_if_using_default_value():
    with pytest.warns(UserWarning) as record:
        check_notebook_source(notebook_ab, {'a': 1})

    assert len(record) == 1
    assert (str(record[0].message)
            == "Missing parameters: {'b'}, will use default value")


def test_error_if_passing_undeclared_parameter():
    with pytest.raises(ValueError) as excinfo:
        check_notebook_source(notebook_ab, {'a': 1, 'b': 2, 'c': 3})

    assert str(excinfo.value) == "\nPassed non-declared parameters: {'c'}"


def test_error_if_using_undeclared_variable():
    notebook_w_warning = """
# + tags=['parameters']
a = 1
b = 2

# +
# variable "c" is used but never declared!
a + b + c
"""
    with pytest.raises(ValueError) as excinfo:
        check_notebook_source(notebook_w_warning, {'a': 1, 'b': 2})

    assert "undefined name 'c'" in str(excinfo.value)


def test_error_if_syntax_error():
    notebook_w_error = """
# + tags=['parameters']
a = 1
b = 2

# +
if
"""
    with pytest.raises(ValueError) as excinfo:
        check_notebook_source(notebook_w_error, {'a': 1, 'b': 2})

    assert 'invalid syntax' in str(excinfo.value)