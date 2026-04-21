import tkinter as tk
from tkinter import ttk, messagebox, font
import math

GEJALA = {
    "G1":  "Nafas abnormal",
    "G2":  "Suara serak",
    "G3":  "Perubahan kulit",
    "G4":  "Telinga penuh",
    "G5":  "Nyeri bicara menelan",
    "G6":  "Nyeri tenggorokan",
    "G7":  "Nyeri leher",
    "G8":  "Pendarahan hidung",
    "G9":  "Telinga berdenging",
    "G10": "Air liur menetes",
    "G11": "Perubahan suara",
    "G12": "Sakit kepala",
    "G13": "Nyeri pinggir hidung",
    "G14": "Serangan vertigo",
    "G15": "Getah bening",
    "G16": "Leher bengkak",
    "G17": "Hidung tersumbat",
    "G18": "Infeksi sinus",
    "G19": "Berat badan turun",
    "G20": "Nyeri telinga",
    "G21": "Selaput lendir merah",
    "G22": "Benjolan leher",
    "G23": "Tubuh tak seimbang",
    "G24": "Bola mata bergerak",
    "G25": "Nyeri wajah",
    "G26": "Dahi sakit",
    "G27": "Batuk",
    "G28": "Tumbuh di mulut",
    "G29": "Benjolan di leher",
    "G30": "Nyeri antara mata",
    "G31": "Radang gendang telinga",
    "G32": "Tenggorokan gatal",
    "G33": "Hidung meler",
    "G34": "Tuli",
    "G35": "Mual muntah",
    "G36": "Letih lesu",
    "G37": "Demam",
}

PENYAKIT = {
    "Tonsilitis":                {"gejala": ["G37","G12","G5","G27","G6","G21"]},
    "Sinusitis Maksilaris":      {"gejala": ["G37","G12","G27","G17","G33","G36","G29"]},
    "Sinusitis Frontalis":       {"gejala": ["G37","G12","G27","G17","G33","G36","G21","G26"]},
    "Sinusitis Edmoidalis":      {"gejala": ["G37","G12","G27","G17","G33","G36","G21","G30","G13","G26"]},
    "Sinusitis Sfenoidalis":     {"gejala": ["G37","G12","G27","G17","G33","G36","G29","G7"]},
    "Abses Peritonsiler":        {"gejala": ["G37","G12","G6","G15","G2","G29","G10"]},
    "Faringitis":                {"gejala": ["G37","G5","G6","G7","G15"]},
    "Kanker Laring":             {"gejala": ["G5","G27","G6","G15","G2","G19","G1"]},
    "Deviasi Septum":            {"gejala": ["G37","G17","G20","G8","G18","G25"]},
    "Laringitis":                {"gejala": ["G37","G5","G15","G16","G32"]},
    "Kanker Leher & Kepala":     {"gejala": ["G5","G22","G8","G28","G3","G11"]},
    "Otitis Media Akut":         {"gejala": ["G37","G20","G35","G31"]},
    "Contact Ulcers":            {"gejala": ["G5","G2"]},
    "Abses Parafaringeal":       {"gejala": ["G5","G16"]},
    "Barotitis Media":           {"gejala": ["G12","G20"]},
    "Kanker Nasofaring":         {"gejala": ["G17","G8"]},
    "Kanker Tonsil":             {"gejala": ["G6","G29"]},
    "Neuronitis Vestibularis":   {"gejala": ["G35","G24"]},
    "Meniere":                   {"gejala": ["G20","G35","G14","G4"]},
    "Tumor Syaraf Pendengaran":  {"gejala": ["G12","G34","G23"]},
    "Kanker Leher Metastatik":   {"gejala": ["G29"]},
    "Osteosklerosis":            {"gejala": ["G34","G9"]},
    "Vertigo Postural":          {"gejala": ["G24"]},
}
def diagnosa(gejala_terpilih: set) -> list:
    """
    Hitung skor kecocokan setiap penyakit dengan gejala yang dipilih.
    Kembalikan list terurut (penyakit, skor%) dari tertinggi ke terendah.
    """
    hasil = []
    for nama, info in PENYAKIT.items():
        ref = set(info["gejala"])
        irisan = gejala_terpilih & ref
        if not irisan:
            continue
        skor = len(irisan) / len(ref) * 100
        hasil.append((nama, round(skor, 1), sorted(irisan), sorted(ref - irisan)))
    hasil.sort(key=lambda x: x[1], reverse=True)
    return hasil


# ═══════════════════════════ APLIKASI GUI ════════════════════════════
class SistemPakarTHT(tk.Tk):
    BG       = "#0f1923"
    SURFACE  = "#162030"
    CARD     = "#1e2d40"
    ACCENT   = "#00c8a0"
    ACCENT2  = "#0099ff"
    TEXT     = "#e8f0fe"
    MUTED    = "#6b7f99"
    DANGER   = "#ff5a6e"
    WARN     = "#ffa94d"
    SUCCESS  = "#00c8a0"
    BORDER   = "#253650"

    def __init__(self):
        super().__init__()
        self.title("Sistem Pakar Diagnosa Penyakit THT")
        self.geometry("1100x720")
        self.minsize(900, 600)
        self.configure(bg=self.BG)
        self._vars: dict[str, tk.BooleanVar] = {}
        self._build_fonts()
        self._build_ui()

    # ── Fonts ──────────────────────────────────────────────────────
    def _build_fonts(self):
        self.f_title  = font.Font(family="Segoe UI", size=18, weight="bold")
        self.f_sub    = font.Font(family="Segoe UI", size=10)
        self.f_label  = font.Font(family="Segoe UI", size=10)
        self.f_bold   = font.Font(family="Segoe UI", size=10, weight="bold")
        self.f_small  = font.Font(family="Segoe UI", size=9)
        self.f_code   = font.Font(family="Consolas",  size=9)
        self.f_result = font.Font(family="Segoe UI", size=13, weight="bold")
        self.f_h3     = font.Font(family="Segoe UI", size=11, weight="bold")

    # ── Layout utama ───────────────────────────────────────────────
    def _build_ui(self):
        # Header
        hdr = tk.Frame(self, bg=self.SURFACE, pady=12)
        hdr.pack(fill="x")
        tk.Label(hdr, text="🏥  Sistem Pakar Diagnosa Penyakit THT",
                 font=self.f_title, bg=self.SURFACE, fg=self.ACCENT).pack()
        tk.Label(hdr, text="Pilih gejala yang dialami pasien, lalu tekan Diagnosa",
                 font=self.f_sub, bg=self.SURFACE, fg=self.MUTED).pack()

        # Body: kiri (gejala) | kanan (hasil)
        body = tk.Frame(self, bg=self.BG)
        body.pack(fill="both", expand=True, padx=16, pady=12)
        body.columnconfigure(0, weight=2)
        body.columnconfigure(1, weight=3)
        body.rowconfigure(0, weight=1)

        self._build_left(body)
        self._build_right(body)

    # ── Panel Kiri: checklist gejala ──────────────────────────────
    def _build_left(self, parent):
        frame = tk.Frame(parent, bg=self.CARD, bd=0)
        frame.grid(row=0, column=0, sticky="nsew", padx=(0,8))
        frame.rowconfigure(1, weight=1)
        frame.columnconfigure(0, weight=1)

        # Header panel
        tk.Label(frame, text="📋  Daftar Gejala", font=self.f_h3,
                 bg=self.CARD, fg=self.TEXT, anchor="w", pady=8, padx=12).grid(
                 row=0, column=0, sticky="ew")
        tk.Frame(frame, bg=self.BORDER, height=1).grid(row=0, column=0,
                 sticky="sew", padx=0)

        # Scrollable checklist
        wrapper = tk.Frame(frame, bg=self.CARD)
        wrapper.grid(row=1, column=0, sticky="nsew")
        wrapper.rowconfigure(0, weight=1)
        wrapper.columnconfigure(0, weight=1)

        canvas = tk.Canvas(wrapper, bg=self.CARD, highlightthickness=0)
        scrollbar = ttk.Scrollbar(wrapper, orient="vertical", command=canvas.yview)
        self.inner = tk.Frame(canvas, bg=self.CARD)

        self.inner.bind("<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.inner, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Mouse-wheel
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(
            int(-1*(e.delta/120)), "units"))

        for i, (kode, nama) in enumerate(sorted(GEJALA.items(),
                                                key=lambda x: int(x[0][1:]))):
            var = tk.BooleanVar()
            self._vars[kode] = var
            bg = self.CARD if i % 2 == 0 else "#192840"
            row_f = tk.Frame(self.inner, bg=bg)
            row_f.pack(fill="x")
            tk.Checkbutton(
                row_f, variable=var,
                bg=bg, activebackground=bg,
                fg=self.TEXT, activeforeground=self.ACCENT,
                selectcolor=self.BG,
                text=f"  {kode}  {nama}",
                font=self.f_label, anchor="w", padx=6, pady=4,
            ).pack(fill="x")

        # Tombol bawah
        btn_frame = tk.Frame(frame, bg=self.CARD, pady=10)
        btn_frame.grid(row=2, column=0, sticky="ew", padx=12)

        tk.Button(btn_frame, text="✔  Diagnosa",
                  font=self.f_bold, bg=self.ACCENT, fg=self.BG,
                  activebackground="#00a882", activeforeground=self.BG,
                  relief="flat", padx=20, pady=8, cursor="hand2",
                  command=self._run_diagnosa).pack(side="left")

        tk.Button(btn_frame, text="↺  Reset",
                  font=self.f_bold, bg=self.BORDER, fg=self.TEXT,
                  activebackground=self.MUTED, relief="flat",
                  padx=16, pady=8, cursor="hand2",
                  command=self._reset).pack(side="left", padx=(10,0))

        self._lbl_terpilih = tk.Label(btn_frame, text="0 gejala dipilih",
                  font=self.f_small, bg=self.CARD, fg=self.MUTED)
        self._lbl_terpilih.pack(side="right")

        # Trace perubahan
        for var in self._vars.values():
            var.trace_add("write", self._update_count)

    # ── Panel Kanan: hasil diagnosa ───────────────────────────────
    def _build_right(self, parent):
        frame = tk.Frame(parent, bg=self.CARD)
        frame.grid(row=0, column=1, sticky="nsew")
        frame.rowconfigure(1, weight=1)
        frame.columnconfigure(0, weight=1)

        tk.Label(frame, text="🔬  Hasil Diagnosa", font=self.f_h3,
                 bg=self.CARD, fg=self.TEXT, anchor="w", pady=8, padx=12).grid(
                 row=0, column=0, sticky="ew")
        tk.Frame(frame, bg=self.BORDER, height=1).grid(row=0, column=0,
                 sticky="sew")

        # Text widget scrollable
        txt_frame = tk.Frame(frame, bg=self.CARD)
        txt_frame.grid(row=1, column=0, sticky="nsew", padx=4, pady=4)
        txt_frame.rowconfigure(0, weight=1)
        txt_frame.columnconfigure(0, weight=1)

        self.txt = tk.Text(txt_frame, bg=self.CARD, fg=self.TEXT,
                           font=self.f_label, wrap="word",
                           relief="flat", padx=16, pady=10,
                           state="disabled", cursor="arrow",
                           highlightthickness=0)
        sb = ttk.Scrollbar(txt_frame, command=self.txt.yview)
        self.txt.configure(yscrollcommand=sb.set)
        self.txt.grid(row=0, column=0, sticky="nsew")
        sb.grid(row=0, column=1, sticky="ns")

        # Tags teks
        self.txt.tag_configure("judul",   font=self.f_result, foreground=self.ACCENT)
        self.txt.tag_configure("rank1",   font=self.f_h3,     foreground=self.ACCENT)
        self.txt.tag_configure("rank2",   font=self.f_h3,     foreground=self.ACCENT2)
        self.txt.tag_configure("rankN",   font=self.f_bold,   foreground=self.TEXT)
        self.txt.tag_configure("persen",  font=self.f_bold,   foreground=self.WARN)
        self.txt.tag_configure("ok",      font=self.f_small,  foreground=self.SUCCESS)
        self.txt.tag_configure("miss",    font=self.f_small,  foreground=self.DANGER)
        self.txt.tag_configure("muted",   font=self.f_small,  foreground=self.MUTED)
        self.txt.tag_configure("info",    font=self.f_label,  foreground=self.TEXT)
        self.txt.tag_configure("warn",    font=self.f_label,  foreground=self.WARN)
        self.txt.tag_configure("bar_fill",font=self.f_code,   foreground=self.ACCENT)
        self.txt.tag_configure("bar_empty",font=self.f_code,  foreground=self.BORDER)

        self._show_placeholder()

    # ── Helper text output ─────────────────────────────────────────
    def _txt_clear(self):
        self.txt.configure(state="normal")
        self.txt.delete("1.0", "end")

    def _txt_write(self, text, tag="info"):
        self.txt.insert("end", text, tag)

    def _txt_done(self):
        self.txt.configure(state="disabled")

    def _show_placeholder(self):
        self._txt_clear()
        self._txt_write("\n\n  Pilih gejala di sebelah kiri,\n"
                        "  lalu tekan  ✔ Diagnosa  untuk melihat hasil.\n", "muted")
        self._txt_done()

    # ── Update counter gejala ──────────────────────────────────────
    def _update_count(self, *_):
        n = sum(1 for v in self._vars.values() if v.get())
        self._lbl_terpilih.configure(text=f"{n} gejala dipilih")

    # ── Reset ──────────────────────────────────────────────────────
    def _reset(self):
        for v in self._vars.values():
            v.set(False)
        self._show_placeholder()

    # ── Progress bar teks ──────────────────────────────────────────
    def _bar(self, persen: float, width=20):
        filled = round(persen / 100 * width)
        return "█" * filled, "░" * (width - filled)

    # ── Diagnosa utama ────────────────────────────────────────────
    def _run_diagnosa(self):
        terpilih = {k for k, v in self._vars.items() if v.get()}
        if not terpilih:
            messagebox.showwarning("Peringatan",
                "Silakan pilih minimal satu gejala terlebih dahulu.")
            return

        hasil = diagnosa(terpilih)

        self._txt_clear()
        self._txt_write("\n  🔬  HASIL DIAGNOSA SISTEM PAKAR THT\n", "judul")
        self._txt_write("  " + "─"*46 + "\n", "muted")

        gejala_list = ", ".join(f"{k}({GEJALA[k]})" for k in sorted(terpilih,
                                key=lambda x: int(x[1:])))
        self._txt_write(f"\n  Gejala yang dipilih ({len(terpilih)}):\n", "muted")
        self._txt_write(f"  {gejala_list}\n\n", "muted")

        if not hasil:
            self._txt_write("  ⚠  Tidak ada penyakit yang cocok dengan "
                            "kombinasi gejala ini.\n", "warn")
            self._txt_write("  Coba tambahkan gejala lain.\n", "muted")
            self._txt_done()
            return

        self._txt_write(f"  Ditemukan {len(hasil)} kemungkinan penyakit:\n\n", "info")

        for i, (nama, skor, cocok, kurang) in enumerate(hasil):
            rank = i + 1
            tag = "rank1" if rank == 1 else ("rank2" if rank == 2 else "rankN")
            medal = ["🥇","🥈","🥉"][i] if i < 3 else f"  {rank}."

            self._txt_write(f"  {medal}  {nama}\n", tag)
            fill, empty = self._bar(skor)
            self._txt_write(f"      ", "info")
            self._txt_write(fill, "bar_fill")
            self._txt_write(empty, "bar_empty")
            self._txt_write(f"  ", "info")
            self._txt_write(f"{skor}%\n", "persen")

            if cocok:
                cocok_str = "  ✔ " + ",  ✔ ".join(
                    f"{k} ({GEJALA[k]})" for k in cocok)
                self._txt_write(f"      {cocok_str}\n", "ok")
            if kurang:
                kurang_str = "  ✘ " + ",  ✘ ".join(
                    f"{k} ({GEJALA[k]})" for k in kurang)
                self._txt_write(f"      {kurang_str}\n", "miss")
            self._txt_write("\n", "info")

        self._txt_write("  " + "─"*46 + "\n", "muted")
        top = hasil[0]
        self._txt_write(f"\n  ✅  Kemungkinan terbesar: ", "info")
        self._txt_write(f"{top[0]}", "rank1")
        self._txt_write(f"  ({top[1]}%)\n", "persen")
        self._txt_write("\n  ⚠  Hasil ini hanya bersifat informatif.\n"
                        "     Konsultasikan dengan dokter THT untuk diagnosis resmi.\n\n",
                        "muted")
        self._txt_done()


# ─────────────────────────── ENTRY POINT ────────────────────────────
if __name__ == "__main__":
    app = SistemPakarTHT()
    app.mainloop()