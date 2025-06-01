from flask import Flask, render_template, request, redirect, url_for, session
from collections import defaultdict

app = Flask(__name__)
app.secret_key = 'kunci_rahasia'

# ===================== GEJALA MATIC =====================
gejala_matic = {
    "G01": "Listrik tidak memberikan signal ketika distater",
    "G02": "Bunyi klakson tidak ada",
    "G03": "Reting tidak berfungsi",
    "G04": "Kondisi listrik kendaraan mati total",
    "G05": "Sulit distater manual",
    "G06": "Knalpot kendaraan meletup",
    "G07": "Tarikan kendaraan terasa berat",
    "G08": "Muncul asap hitam dari knalpot",
    "G09": "Mesin lebih mudah panas",
    "G010": "Boros penggunaan bahan bakar",
    "G011": "Bunyi usik pada mesin",
    "G012": "Suara mesin terdengar keras/kasar",
    "G013": "Kecepatan tempuh kendaraan tidak optimal",
    "G014": "Bunyi kendaraan tidak nyaman ketika jalan perlahan",
    "G015": "Kompas kopling lambat",
    "G016": "Lari kendaraan tersedak-sedak",
    "G017": "Kendaraan tiba-tiba mati total",
    "G018": "Tidak stabilnya tarikan gas",
    "G019": "Lampu indikator kendaraan nyala terus",
    "G020": "Lampu depan sering mati",
    "G021": "Rem motor tidak terlalu berfungsi",
    "G022": "Motor tidak mampu menempuh ketinggian yang terbilang normal",
    "G023": "Oli menetes tiba-tiba",
    "G024": "Motor sering terasa tidak seimbang",
    "G025": "Bohlam lampu sering putus"
}

# ===================== GEJALA GIGI =====================
gejala_gigi = {
    "G1": "Saat sepeda motor diengkol/distarter mesin tidak hidup/mati",
    "G2": " Motor tidak mau hidup pada hal bensin penuh",
    "G3": " Saat diengkol terasa ringan atau kosong",
    "G4": "Saat dinyalakan lampu indikator motor tdak menyala",
    "G5": "Lampu – Lampu sepeda motor redup dan tidak menyala",
    "G6": "Saat di starter mesin Motor tidak hidup tapi saat di engkol motor dapat hidup",
    "G7": "Saat berjalan motor teresa tersendat sendat dan tarikan gas tidak responsif",
    "G8": " Bensin terasa cepat berkurang atau bertambah boros",
    "G9": "Kabel dari CDI tidak mengeluarkan arus listrik",
    "G10": "Kabel Koil tidak mengeluarkan arus listrik",
    "G11": "Saat tombal starter ditekan tidak terdengar suara dinamo atau terdengar tapi mesin motor tidak hidup",
    "G12": "Dalam kondisi aki masih bagus saat tombol starter ditekan mesin motor tidak mau hidup",
    "G13": " Timbul suara mengelitik pada Kepala mesin / cylender head",
    "G14": "Timbul suara berisik pada kepala mesin / cylender head pada bagian depan",
    "G15": "Akselerasi mesin melemah dan mesin terasa cepat panas",
    "G16": " Mesin kasar ketika kecepatan tinggi dan perpindahan gigi sulit",
    "G17": "Kondisi noken as masih bagus tetapi kepala mesin/cylender head masih ada suara berisik",
    "G18": "Kondisi kleb masih bagus tetapi suara kepala mesin/ cylender head masih terdengar berisik",
    "G19": "Timbulnya suara pada mesin gemericik yang berisik pada mesin",
    "G20": " kondisi otomatis tensioner masih normal tapi ada suara gemericik pada mesin",
    "G21": "Pada saat ganti oli, oli terlihat kotor terdapat bekas hancuran karet",
    "G22": "Mesin motor terasa bergetar",
    "G23": "Terdengar suara kasar yang cukup keras pada mesin",
    "G24": "Keluar asap putih dari kenalpot pada saat start",
    "G25": "Keluar asap putih tebal dari kenalpot",
    "G26": "Timbulnya getaran pada saat motor berjalan",
    "G27": "Bagian depan sepeda motor bergetar dan berbunyi saat di jalan berlubang atau kasar",
    "G28": "Bagian belakang sepeda motor terasa berat dan kurang fleksibel saat berkendara terasa kaku dan bergetar",
    "G29": "Motor terasa tidak stabil ",
    "G30": " Terdapat suara menggangu pada bagian pedal injak"
}

# Gabungkan semua gejala
gejala_dict = {**gejala_matic, **gejala_gigi}

# ===================== ATURAN MATIC =====================
aturan_matic = {
    "A01": {"gejala": ["G01", "G02", "G03", "G04"], "penyakit": "P01"},
    "A02": {"gejala": ["G05", "G06", "G07", "G08"], "penyakit": "P02"},
    "A03": {"gejala": ["G07", "G09", "G019", "G020"], "penyakit": "P03"},
    "A04": {"gejala": ["G01", "G05", "G07", "G020"], "penyakit": "P04"},
    "A05": {"gejala": ["G05", "G07", "G011", "G012", "G025"], "penyakit": "P05"},
    "A06": {"gejala": ["G07", "G014", "G015", "G012", "G013", "G024"], "penyakit": "P06"},
    "A07": {"gejala": ["G016", "G017", "G018", "G023"], "penyakit": "P07"}
}

# ===================== ATURAN GIGI =====================
aturan_gigi = {
    "R1": {"gejala": ["G1", "G2", "G3"], "penyakit": "KM1", },
    "R2": {"gejala": ["G4", "G5", "G6"], "penyakit": "KM2"},
    "R3": {"gejala": ["G7", "G8"], "penyakit": "KM3"},
    "R4": {"gejala": ["G9"], "penyakit": "KM4"},
    "R5": {"gejala": ["G10"], "penyakit": "KM5"},
    "R6": {"gejala": ["G11", "G12"], "penyakit": "KM6"},
    "R7": {"gejala": ["G13", "G14"], "penyakit": "KM7"},
    "R8": {"gejala": ["G15", "G16"], "penyakit": "KM8"},
    "R9": {"gejala": ["G17", "G18"], "penyakit": "KM9"},
    "R10": {"gejala": ["G19", "G20"], "penyakit": "KM10"},
    "R11": {"gejala": ["G21", "G22", "G23"], "penyakit": "KM11"},
    "R12": {"gejala": ["G24", "G25"], "penyakit": "KM12"},
    "R13": {"gejala": ["G26", "G27"], "penyakit": "KM13"},
    "R14": {"gejala": ["G28"], "penyakit": "KM14"},
    "R15": {"gejala": ["G29", "G30"], "penyakit": "KM15"},
}

# ===================== PENYAKIT MATIC =====================
penyakit_matic_dict = {
    "P01" : "ACU",
    "P02" : "Busi",
    "P03" : "Celah Klep",
    "P04" : "Injector",
    "P05" : "Roller",
    "P06" : "CVT",
    "P07" : "ECM"
}

# ===================== NAMA PENYAKIT GIGI =====================
penyakit_gigi_dict = {
    "KM1": "Busi",
    "KM2": "Aki",
    "KM3": "Karbu",
    "KM4": "CDI",
    "KM5": "Koil",
    "KM6": "Dinamo Stater",
    "KM7": "Kleb",
    "KM8": "Kopling",
    "KM9": "Bos Kleb",
    "KM10": "Tensioner",
    "KM11": "Rantai Keteng",
    "KM12": "Piston",
    "KM13": "Shock Depan",
    "KM14": "Shock Belakang",
    "KM15": "Swing ARM goyang atau baut aus",
}



# ===================== GABUNGKAN SEMUA ATURAN =====================
aturan_semua = {**aturan_matic, **aturan_gigi}


# ===================== ROUTES =====================

@app.route('/')
def index():
    # Reset session setiap kali user kembali ke halaman awal
    session.clear()
    return render_template('index.html')

@app.route('/pertanyaan', methods=['GET', 'POST'])
def pertanyaan():
    if 'jawaban' not in session:
        session['jawaban'] = {}
        session['aturan_index'] = 0
        session['gejala_index'] = 0

    if 'jenis_motor' not in session:
        if request.method == 'POST':
            session['jenis_motor'] = request.form['jawaban']
            return redirect(url_for('pertanyaan'))
        return render_template('pertanyaan.html', is_type_selection=True, pertanyaan="Pilih jenis motor", nomor=1, total=1)

    # Ambil aturan sesuai jenis motor
    aturan = list(aturan_matic.items()) if session['jenis_motor'] == 'matic' else list(aturan_gigi.items())

    while session['aturan_index'] < len(aturan):
        kode_aturan, data = aturan[session['aturan_index']]
        gejala_list = data['gejala']
        current_index = session['gejala_index']

        if current_index < len(gejala_list):
            kode_gejala = gejala_list[current_index]

            if kode_gejala in session['jawaban']:
                if session['jawaban'][kode_gejala] == 'tidak':
                    session['aturan_index'] += 1
                    session['gejala_index'] = 0
                else:
                    session['gejala_index'] += 1
                return redirect(url_for('pertanyaan'))

            if request.method == 'POST':
                jawaban = request.form['jawaban']
                kode = request.form['kode']
                session['jawaban'][kode] = jawaban

                if jawaban == 'tidak':
                    session['aturan_index'] += 1
                    session['gejala_index'] = 0
                else:
                    session['gejala_index'] += 1
                return redirect(url_for('pertanyaan'))

            return render_template(
                'pertanyaan.html',
                kode=kode_gejala,
                pertanyaan=f"Apakah motor mengalami gejala: {gejala_dict.get(kode_gejala, kode_gejala)}?",
                nomor=len(session['jawaban']) + 1,
                total=len(gejala_list),
                is_type_selection=False
            )
        else:
            # Semua gejala dalam aturan ini dijawab "ya" → diagnosa ditemukan
            session['penyakit'] = data['penyakit']
            if session['penyakit'].startswith("KM"):
                session['nama_penyakit'] = penyakit_gigi_dict.get(session['penyakit'], session['penyakit'])
            elif session['penyakit'].startswith("P0"):
                session['nama_penyakit'] = penyakit_matic_dict.get(session['penyakit'], session['penyakit'])
            else:
                session['nama_penyakit'] = session['penyakit']

            return redirect(url_for('hasil'))

    # Jika semua aturan telah dicoba dan tidak ada yang cocok
    session['penyakit'] = "Tidak ditemukan diagnosa yang cocok."
    session['nama_penyakit'] = "Tidak ditemukan diagnosa yang cocok."
    return redirect(url_for('hasil'))


@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('pertanyaan'))

@app.route('/hasil')
def hasil():
    try:
        jawaban = session.get('jawaban', {})
        print("=== DEBUG: Jawaban pengguna ===")
        print(jawaban)
        print("================================")

        diagnosa_results = []
        best_rule = None

        for kode_aturan, data_aturan in aturan_semua.items():
            if not isinstance(data_aturan, dict):
                print(f"Skipping {kode_aturan} because data_aturan is not a dict: {data_aturan}")
                continue

            gejala_list = data_aturan.get('gejala')
            if not isinstance(gejala_list, list):
                print(f"Skipping {kode_aturan} because 'gejala' is missing or not a list: {gejala_list}")
                continue

            cocok = all(jawaban.get(g, 'tidak') == 'ya' for g in gejala_list)
            if cocok:
                penyakit = data_aturan.get('penyakit')

                if penyakit.startswith("KM"):
                    nama_penyakit = penyakit_gigi_dict.get(penyakit, penyakit)
                elif penyakit.startswith("P0"):
                    nama_penyakit = penyakit_matic_dict.get(penyakit, penyakit)
                else:
                    nama_penyakit = penyakit

                if best_rule is None or len(gejala_list) > len(aturan_semua[best_rule['kode_aturan']]['gejala']):
                    best_rule = {
                        "kode_aturan": kode_aturan,
                        "penyakit": nama_penyakit,
                    }

        if best_rule:
            diagnosa_results.append(best_rule)
        else:
            diagnosa_results.append({
                "kode_aturan": None,
                "penyakit": "Tidak ditemukan diagnosa yang cocok.",
            })

        return render_template('hasil.html', diagnosa_results=diagnosa_results)

    except Exception as e:
        print(f"Exception in /hasil route: {e}")
        return f"<h1>Terjadi kesalahan pada server:</h1><p>{e}</p>", 500



@app.route('/tentang')
def tentang():
    return render_template('tentang.html')

@app.route('/layanan')
def layanan():
    return render_template('layanan.html')

@app.route('/edukasi')
def edukasi():
    return render_template('edukasi.html')

if __name__ == '__main__':
    app.run(debug=True)