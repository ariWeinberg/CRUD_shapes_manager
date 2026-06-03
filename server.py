import dynamic_shapes  # noqa: F401
import shape_manager_errors
from fastapi import FastAPI, Depends, HTTPException
from pydantic import Field
from dynamic_shape_managment.dynamic_shape_type_manager import DynamicShapeTypeManager
from typing import Annotated, Union
import uvicorn
from shape_manager import ShapeManager


def init_db_connection():
    shape_manager = ShapeManager()

    def get_db_connection():
        return shape_manager
    return get_db_connection


get_db_connection = init_db_connection()

creation_models = [shape.shape_creation_model for shape in DynamicShapeTypeManager.shape_descriptors]
response_models = [shape.shape_response_model[0] for shape in DynamicShapeTypeManager.shape_descriptors]
update_models = [shape.shape_update_model[0] for shape in DynamicShapeTypeManager.shape_descriptors]


AnyShapeCreation = Annotated[Union[*creation_models], Field(discriminator="shape_type")]

AnyShapeResponse = Annotated[Union[*response_models], Field(discriminator="shape_type")]

AnyShapeUpdate = Annotated[Union[*update_models], Field(discriminator="shape_type")]

app = FastAPI()


@app.get("/shapes", response_model=list[AnyShapeResponse])
def get_all_shapes(sort: bool | None = None, filter_type: str | None = None, shape_manager: ShapeManager = Depends(get_db_connection)):
    return shape_manager.get_all_shapes(type_filter=filter_type, sort_direction=sort)


@app.get("/shapes/total-area")
def get_shapes_total_area(
    shape_manager: ShapeManager = Depends(get_db_connection)
):
    return {"shapes_total_area": sum([shape.get_area() for shape in shape_manager.get_all_shapes()] or 0)}


@app.get("/shapes/{shape_id}", response_model=AnyShapeResponse)
def get_shape_by_id(
        shape_id: int,
        shape_manager: ShapeManager = Depends(get_db_connection)
        ):
    try:
        shape = shape_manager.get_shape_by_id(shape_id=shape_id)
    except shape_manager_errors.ShapeManagerShapeNotFoundError as e:
        raise HTTPException(404, str(e))

    descriptor = DynamicShapeTypeManager.get_shape_descriptor(shape.shape_type)
    return descriptor.shape_response_model[0].from_domain(shape)


@app.put("/shapes/{shape_id}", response_model=AnyShapeResponse)
def update_shape(
        shape_id: int,
        new_shape: AnyShapeCreation,
        shape_manager: ShapeManager = Depends(get_db_connection)
        ):
    new_shape = new_shape.to_domain()
    try:
        shape_manager.update_shape(shape_id=shape_id, new_data=new_shape)
    except shape_manager_errors.ShapeManagerShapeNotFoundError as e:
        raise HTTPException(404, str(e))

    descriptor = DynamicShapeTypeManager.get_shape_descriptor(new_shape.shape_type)
    return descriptor.shape_response_model[0].from_domain(new_shape)


@app.post("/shapes", response_model=AnyShapeResponse)
def create_shape(
        shape: AnyShapeCreation,
        shape_manager: ShapeManager = Depends(get_db_connection)
        ) -> None:

    new_shape = shape.to_domain()
    shape_manager.create_shape(new_shape)

    descriptor = DynamicShapeTypeManager.get_shape_descriptor(new_shape.shape_type)
    return descriptor.shape_response_model[0].from_domain(new_shape)


@app.delete("/shapes/{shape_id}")
def delete_shape(
        shape_id: int,
        shape_manager: ShapeManager = Depends(get_db_connection)
        ):
    try:
        shape_manager.delete_shape(shape_id=shape_id)
    except shape_manager_errors.ShapeManagerShapeNotFoundError as e:
        raise HTTPException(404, str(e))
    return {"message": f"shape: {shape_id} deleted successfully."}


uvicorn.run(app, port=8086)
