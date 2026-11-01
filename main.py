"""Sistem Manajemen Warnet Sederhana (berorientasi objek)."""
from datetime import datetime
from math import ceil


def rupiah(angka):
    return "Rp" + f"{angka:,}".replace(",", ".")


class Komputer:
    """PC biasa. Atribut kelas (jenis, tarif) bisa ditimpa oleh subclass."""
    jenis = "Reguler"
    tarif_per_jam = 5000

    def __init__(self, nomor):
        self.nomor = nomor
        self.sesi = None  # None berarti PC sedang kosong

    @property
    def terpakai(self):
        return self.sesi is not None

    def __str__(self):
        status = f"dipakai {self.sesi.pelanggan}" if self.terpakai else "kosong"
        return f"PC-{self.nomor:02d} [{self.jenis}] {rupiah(self.tarif_per_jam)}/jam - {status}"


class KomputerVIP(Komputer):
    """Pewarisan: sama seperti Komputer, tetapi spesifikasi dan tarif lebih tinggi."""
    jenis = "VIP"
    tarif_per_jam = 8000


class Sesi:
    """Satu kali pemakaian PC oleh seorang pelanggan."""

    def __init__(self, pelanggan, komputer):
        self.pelanggan = pelanggan
        self.komputer = komputer
        self.mulai = datetime.now()

    def hitung_biaya(self):
        detik = (datetime.now() - self.mulai).total_seconds()
        menit = max(1, ceil(detik / 60))  # minimal 1 menit, dibulatkan ke atas
        return menit, round(menit * self.komputer.tarif_per_jam / 60)


class Warnet:
    """Mengelola daftar PC, sesi yang berjalan, dan riwayat pendapatan."""

    def __init__(self, jumlah_reguler=5, jumlah_vip=2):
        self.daftar_pc = [Komputer(i) for i in range(1, jumlah_reguler + 1)]
        self.daftar_pc += [KomputerVIP(i) for i in range(jumlah_reguler + 1, jumlah_reguler + jumlah_vip + 1)]
        self.riwayat = []  # berisi (pelanggan, nomor PC, menit, biaya)

    def cari_pc(self, nomor):
        for pc in self.daftar_pc:
            if pc.nomor == nomor:
                return pc
        raise ValueError(f"PC nomor {nomor} tidak ada.")

    def mulai_sesi(self, nomor, pelanggan):
        pc = self.cari_pc(nomor)
        if pc.terpakai:
            raise ValueError(f"PC-{nomor:02d} sedang dipakai.")
        pc.sesi = Sesi(pelanggan, pc)

    def akhiri_sesi(self, nomor):
        pc = self.cari_pc(nomor)
        if not pc.terpakai:
            raise ValueError(f"PC-{nomor:02d} sedang kosong.")
        menit, biaya = pc.sesi.hitung_biaya()
        self.riwayat.append((pc.sesi.pelanggan, nomor, menit, biaya))
        pc.sesi = None
        return menit, biaya

    def total_pendapatan(self):
        return sum(r[3] for r in self.riwayat)


def baca_nomor(teks):
    try:
        return int(input(teks))
    except ValueError:
        raise ValueError("Nomor PC harus berupa angka.")


def main():
    warnet = Warnet()
    menu = "\n=== WARNET ===\n1. Lihat daftar PC\n2. Mulai sesi\n3. Akhiri sesi & bayar\n4. Laporan pendapatan\n0. Keluar"
    while True:
        print(menu)
        pilihan = input("Pilih menu: ").strip()
        try:
            if pilihan == "1":
                for pc in warnet.daftar_pc:
                    print(pc)
            elif pilihan == "2":
                nomor = baca_nomor("Nomor PC: ")
                warnet.mulai_sesi(nomor, input("Nama pelanggan: ").strip() or "Tamu")
                print("Sesi dimulai.")
            elif pilihan == "3":
                menit, biaya = warnet.akhiri_sesi(baca_nomor("Nomor PC: "))
                print(f"Durasi {menit} menit, total bayar {rupiah(biaya)}.")
            elif pilihan == "4":
                print(f"Transaksi: {len(warnet.riwayat)} | Pendapatan: {rupiah(warnet.total_pendapatan())}")
                for pelanggan, nomor, menit, biaya in warnet.riwayat:
                    print(f"- {pelanggan} (PC-{nomor:02d}, {menit} menit): {rupiah(biaya)}")
            elif pilihan == "0":
                print("Terima kasih.")
                break
            else:
                print("Menu tidak valid.")
        except ValueError as galat:
            print("Gagal:", galat)


if __name__ == "__main__":
    main()