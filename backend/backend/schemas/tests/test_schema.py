import pytest
from pydantic import ValidationError
from schema import Schema


# Test valid YAML data
def test_valid_schema():
    yaml_data = {
        "dataset": {
            "name": "employees",
            "dimensions": [
                {
                    "name": "employee_id",
                    "type": "integer",
                    "description": "Unique identifier for each employee",
                },
                {"name": "name", "type": "string", "description": "Employee's name"},
            ],
            "measures": [
                {
                    "name": "total_employees",
                    "type": "integer",
                    "aggregation": "count",
                    "description": "Total number of employees",
                }
            ],
            "views": [
                {
                    "name": "employee_overview",
                    "description": "A view combining employees with departments",
                    "joins": [
                        {
                            "dataset": "departments",
                            "on": "employees.department_id = departments.id",
                        }
                    ],
                }
            ],
        }
    }

    schema = Schema(**yaml_data)
    assert schema.dataset.name == "employees"
    assert len(schema.dataset.dimensions) == 2
    assert len(schema.dataset.measures) == 1
    assert len(schema.dataset.views) == 1


# Test invalid schema with duplicate dimension names
def test_invalid_schema_duplicate_dimensions():
    yaml_data = {
        "dataset": {
            "name": "employees",
            "dimensions": [
                {
                    "name": "employee_id",
                    "type": "integer",
                    "description": "Unique identifier for each employee",
                },
                {
                    "name": "employee_id",
                    "type": "string",
                    "description": "Duplicate dimension name",
                },
            ],
            "measures": [
                {
                    "name": "total_employees",
                    "type": "integer",
                    "aggregation": "count",
                    "description": "Total number of employees",
                }
            ],
            "views": [],
        }
    }

    with pytest.raises(ValidationError) as excinfo:
        Schema(**yaml_data)

    assert "Dimension names must be unique within a dataset" in str(excinfo.value)


# Test invalid schema with duplicate measure names
def test_invalid_schema_duplicate_measures():
    yaml_data = {
        "dataset": {
            "name": "employees",
            "dimensions": [
                {
                    "name": "employee_id",
                    "type": "integer",
                    "description": "Unique identifier for each employee",
                }
            ],
            "measures": [
                {
                    "name": "total_employees",
                    "type": "integer",
                    "aggregation": "count",
                    "description": "Total number of employees",
                },
                {
                    "name": "total_employees",
                    "type": "float",
                    "aggregation": "sum",
                    "description": "Duplicate measure name",
                },
            ],
            "views": [],
        }
    }

    with pytest.raises(ValidationError) as excinfo:
        Schema(**yaml_data)

    assert "Measure names must be unique within a dataset" in str(excinfo.value)


# Test invalid schema with incorrect type in dimension
def test_invalid_schema_dimension_type():
    yaml_data = {
        "dataset": {
            "name": "employees",
            "dimensions": [
                {
                    "name": "employee_id",
                    "type": "invalid_type",
                    "description": "Invalid type for dimension",
                }
            ],
            "measures": [],
            "views": [],
        }
    }

    with pytest.raises(ValidationError) as excinfo:
        Schema(**yaml_data)

    assert "unexpected value; permitted: 'integer', 'string', 'float', 'date'" in str(
        excinfo.value
    )


# Test invalid schema with incorrect type in measure
def test_invalid_schema_measure_type():
    yaml_data = {
        "dataset": {
            "name": "employees",
            "dimensions": [],
            "measures": [
                {
                    "name": "total_employees",
                    "type": "invalid_type",
                    "aggregation": "count",
                    "description": "Invalid type for measure",
                }
            ],
            "views": [],
        }
    }

    with pytest.raises(ValidationError) as excinfo:
        Schema(**yaml_data)

    assert "unexpected value; permitted: 'integer', 'float'" in str(excinfo.value)


# Test invalid schema with incorrect aggregation in measure
def test_invalid_schema_measure_aggregation():
    yaml_data = {
        "dataset": {
            "name": "employees",
            "dimensions": [],
            "measures": [
                {
                    "name": "total_employees",
                    "type": "integer",
                    "aggregation": "invalid_aggregation",
                    "description": "Invalid aggregation for measure",
                }
            ],
            "views": [],
        }
    }

    with pytest.raises(ValidationError) as excinfo:
        Schema(**yaml_data)

    assert "unexpected value; permitted: 'count', 'sum', 'avg', 'min', 'max'" in str(
        excinfo.value
    )
