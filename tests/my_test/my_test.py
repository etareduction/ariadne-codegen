import ast
from typing import cast

from graphql import (
    FragmentDefinitionNode,
    OperationDefinitionNode,
    build_ast_schema,
    parse,
    print_ast,
)

from ariadne_codegen.client_generators.constants import BASE_MODEL_CLASS_NAME
from ariadne_codegen.client_generators.constants import MIXIN_NAME
from ariadne_codegen.client_generators.result_types import ResultTypesGenerator

from ..utils import format_graphql_str
from ..utils import compare_ast
from .schema import SCHEMA_STR


def test_my_test():
    query_str = format_graphql_str(
        """
        query CustomQuery {
            query4 {
                ... on CustomType1 {
                    fielda
                    fieldc
                }
            }
        }
        """
    )
    expected_result = """from typing import Optional, Union, Any, List, Literal, Annotated
from pydantic import Field, BeforeValidator
from pydantic import BaseModel

class CustomQuery(BaseModel):
    query_4: Union["CustomQueryQuery4CustomType1", "CustomQueryQuery4CustomType2"] = Field(alias='query4', discriminator='typename__')

class CustomQueryQuery4CustomType1(BaseModel):
    typename__: Literal["CustomType1"] = Field(alias='__typename')
    fielda: int
    fieldc: Optional[int]

class CustomQueryQuery4CustomType2(BaseModel):
    typename__: Literal["CustomType2"] = Field(alias='__typename')
CustomQuery.model_rebuild()"""
    generator = ResultTypesGenerator(
        schema=build_ast_schema(parse(SCHEMA_STR)),
        operation_definition=cast(
            OperationDefinitionNode, parse(query_str).definitions[0]
        ),
        enums_module_name="enums",
        default_optional_fields_to_none=False,
    )
    result = generator.generate()
    print(ast.unparse(result))
    assert expected_result==ast.unparse(result)

def test_my_test2():
    query_str = format_graphql_str(
        """
        query CustomQuery {
            query4 {
                ... on CustomType1 {
                    fielda
                    fieldc
                }
            }
        }
        """
    )
    expected_result = """from typing import Optional, Union, Any, List, Literal, Annotated
from pydantic import Field, BeforeValidator
from pydantic import BaseModel

class CustomQuery(BaseModel):
    query_4: Union["CustomQueryQuery4CustomType1", "CustomQueryQuery4CustomType2"] = Field(alias='query4', discriminator='typename__')

class CustomQueryQuery4CustomType1(BaseModel):
    typename__: Literal["CustomType1"] = Field(alias='__typename')
    fielda: int
    fieldc: Optional[int] = Field(default=None)

class CustomQueryQuery4CustomType2(BaseModel):
    typename__: Literal["CustomType2"] = Field(alias='__typename')
CustomQuery.model_rebuild()"""
    generator = ResultTypesGenerator(
        schema=build_ast_schema(parse(SCHEMA_STR)),
        operation_definition=cast(
            OperationDefinitionNode, parse(query_str).definitions[0]
        ),
        enums_module_name="enums",
        default_optional_fields_to_none=True,
    )
    result = generator.generate()
    print(ast.unparse(result))
    assert expected_result==ast.unparse(result)