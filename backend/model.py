from pydantic import BaseModel

class Barang(BaseModel):
    id: int = None
    nama: str
    kategori: str
    jumlah_stok: int
    lokasi_gudang: str