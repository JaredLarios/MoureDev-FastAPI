from fastapi import APIRouter

router = APIRouter(prefix="/products",
                   tags=["products"],
                   responses={404: {"message":"not found"}})

@router.get("/products/")
async def products():
    return {"urls":"jeddevcenter.github.com/urls"}