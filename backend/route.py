from fastapi import APIRouter, HTTPException
import model
import database

router = APIRouter()

@router.get("/")
def get_all_barang():
    return database.inventory_db

@router.post("/")
def tambah_barang(barang: model.Barang):
    new_id = max([b['id'] for b in database.inventory_db], default=0) + 1
    barang_dict = barang.dict()
    barang_dict['id'] = new_id
    database.inventory_db.append(barang_dict)
    return {"message": "Data berhasil ditambahkan", "data": barang_dict}

@router.delete("/{barang_id}")
def hapus_barang(barang_id: int):
    for i, b in enumerate(database.inventory_db):
        if b['id'] == barang_id:
            deleted_item = database.inventory_db.pop(i)
            return {"message": "Data berhasil dihapus", "data": deleted_item}
    raise HTTPException(status_code=404, detail="Barang tidak ditemukan")

@router.put("/{barang_id}")
def update_barang(barang_id: int, barang_update: model.Barang):
    for i, b in enumerate(database.inventory_db):
        if b['id'] == barang_id:
            updated_data = barang_update.dict()
            updated_data['id'] = barang_id
            database.inventory_db[i] = updated_data
            return {"message": "Data berhasil diubah", "data": updated_data}
    raise HTTPException(status_code=404, detail="Barang tidak ditemukan")