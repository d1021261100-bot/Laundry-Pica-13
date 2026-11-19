import streamlit as st

st.set_page_config(page_title="Laundry Kiloan", page_icon="🧺")

if "nim" not in st.session_state:
    st.session_state.nim = ""
if "berat" not in st.session_state:
    st.session_state.berat = 0
if "hasil" not in st.session_state:
    st.session_state.hasil = None


def format_rupiah(angka):
    return "Rp " + f"{angka:,.0f}".replace(",", ".")


def reset():
    st.session_state.nim = ""
    st.session_state.berat = 0
    st.session_state.hasil = None


def hitung():
    nim = st.session_state.nim
    berat = st.session_state.berat

    if len(nim) != 10 or not nim.isdigit():
        st.session_state.hasil = ("error", "NIM tidak valid! NIM harus terdiri dari tepat 10 digit angka.")
        return

    if berat <= 0:
        st.session_state.hasil = ("error", "Berat cucian harus lebih dari 0 kg.")
        return

    digit_genap = 0
    for d in nim:
        if int(d) % 2 == 0:
            digit_genap += 1

    digit_terakhir = int(nim[-1])
    tarif = 5000 + (digit_terakhir * 500)
    persen_diskon = digit_genap * 1
    biaya_normal = berat * tarif
    potongan = persen_diskon / 100 * biaya_normal
    total = biaya_normal - potongan

    st.session_state.hasil = (
        "ok",
        {
            "tarif": tarif,
            "genap": digit_genap,
            "diskon": persen_diskon,
            "normal": biaya_normal,
            "potongan": potongan,
            "total": total,
        },
    )


st.title("🧺 Laundry Kiloan")
st.caption("Hitung cepat biaya laundry kiloan")

st.text_input("NIM (10 digit)", key="nim", max_chars=10)
st.number_input("Berat Cucian (kg)", key="berat", step=1)

kol1, kol2 = st.columns(2)
kol1.button("Hitung", on_click=hitung, use_container_width=True)
kol2.button("Reset", on_click=reset, use_container_width=True)

if st.session_state.hasil is not None:
    status, isi = st.session_state.hasil

    if status == "error":
        st.error(isi)
    else:
        st.subheader("Hasil Perhitungan")
        st.write(f"Tarif per kg : {format_rupiah(isi['tarif'])}")
        st.write(f"Jumlah digit genap : {isi['genap']}")
        st.write(f"Persen diskon : {isi['diskon']} %")
        st.write(f"Biaya normal : {format_rupiah(isi['normal'])}")
        st.write(f"Potongan : {format_rupiah(isi['potongan'])}")
        st.success(f"Total bayar : {format_rupiah(isi['total'])}")