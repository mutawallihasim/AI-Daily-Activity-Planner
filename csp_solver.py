class Activity:
    """
    Representasi data aktivitas harian mahasiswa.
    """
    def __init__(self, name, category, duration, fixed_start=None, id=None):
        self.name = name
        self.category = category  # "Jam Kuliah Tetap", "Waktu Tugas/Belajar Mandiri", "Agenda Organisasi", "Waktu Istirahat"
        self.duration = duration
        self.fixed_start = fixed_start  # Jam mulai (int, misal 8 untuk 08:00), None jika fleksibel
        self.id = id if id else f"{category.lower().replace(' ', '_')}_{name.lower().replace(' ', '_')}"

    def __repr__(self):
        return f"Activity({self.name}, {self.category}, {self.duration}h, fixed={self.fixed_start})"


def solve_csp_library(activities):
    """
    Menyelesaikan CSP menggunakan pustaka python-constraint.
    """
    from constraint import Problem

    problem = Problem()
    
    # 1. Menambahkan variabel dan domainnya
    for act in activities:
        if act.fixed_start is not None:
            # Jika waktu mulai tetap, domainnya hanya jam tersebut
            domain = [act.fixed_start]
        else:
            # Jika fleksibel, domain adalah seluruh jam mulai yang memungkinkan dalam siklus 07:00 - 22:00
            domain = list(range(7, 22 - act.duration + 1))
        
        problem.addVariable(act.id, domain)

    # 2. Menambahkan batasan tidak boleh saling tumpang tindih (Overlap Constraint)
    # Untuk setiap pasang aktivitas, interval waktu kerjanya tidak boleh berbenturan
    for i in range(len(activities)):
        for j in range(i + 1, len(activities)):
            act1 = activities[i]
            act2 = activities[j]
            
            problem.addConstraint(
                lambda s1, s2, d1=act1.duration, d2=act2.duration: s1 + d1 <= s2 or s2 + d2 <= s1,
                (act1.id, act2.id)
            )

    # 3. Mencari solusi
    solutions = problem.getSolutions()
    if not solutions:
        return None

    # Mengambil solusi pertama dan memetakan ke jadwal per jam
    sol = solutions[0]
    schedule = {h: "Kosong" for h in range(7, 22)}
    for act in activities:
        start = sol[act.id]
        for h in range(start, start + act.duration):
            schedule[h] = act.name
            
    return schedule


def solve_csp_custom(activities):
    """
    Menyelesaikan CSP menggunakan algoritma Backtracking Search kustom
    dan menghasilkan log langkah demi langkah untuk visualisasi.
    """
    variables = [act.id for act in activities]
    act_map = {act.id: act for act in activities}
    
    # Menentukan domain untuk setiap variabel
    domains = {}
    for act in activities:
        if act.fixed_start is not None:
            domains[act.id] = [act.fixed_start]
        else:
            domains[act.id] = list(range(7, 22 - act.duration + 1))

    log_steps = []
    step_counter = [0]

    def log_step(step_type, var_id, val, assignment, message):
        step_counter[0] += 1
        
        # Membuat timeline representasi visual saat ini
        schedule = {h: "Kosong" for h in range(7, 22)}
        # Pertama, masukkan aktivitas yang sudah berhasil terpasang di assignment
        for assigned_var, start in assignment.items():
            assigned_act = act_map[assigned_var]
            for h in range(start, start + assigned_act.duration):
                schedule[h] = assigned_act.name

        log_steps.append({
            "step_num": step_counter[0],
            "type": step_type,
            "variable_name": act_map[var_id].name,
            "variable_category": act_map[var_id].category,
            "variable_id": var_id,
            "value": val,
            "assignment": assignment.copy(),
            "schedule": schedule,
            "message": message
        })

    def is_consistent(var_id, val, assignment):
        act = act_map[var_id]
        start = val
        end = val + act.duration
        
        # Cek bentrokan dengan semua variabel yang sudah di-assign sebelumnya
        for other_var, other_start in assignment.items():
            if other_var == var_id:
                continue
            other_act = act_map[other_var]
            other_end = other_start + other_act.duration
            
            # Jika overlap
            if start < other_end and other_start < end:
                return False, f"Bentrok dengan {other_act.name} ({other_start:02d}.00 - {other_end:02d}.00)"
        return True, "Konsisten"

    def backtrack(assignment):
        # Jika semua variabel sudah berhasil dipetakan, pencarian selesai
        if len(assignment) == len(variables):
            return assignment
            
        # Pemilihan variabel berikutnya (menggunakan heuristik MRV - Minimum Remaining Values)
        unassigned = [v for v in variables if v not in assignment]
        unassigned.sort(key=lambda v: len(domains[v]))
        var_id = unassigned[0]
        act = act_map[var_id]
        
        # Coba setiap nilai di domain variabel tersebut
        for val in domains[var_id]:
            # Log percobaan penugasan
            log_step("assign", var_id, val, assignment, f"Mencoba menjadwalkan {act.name} pada pukul {val:02d}.00")
            
            consistent, reason = is_consistent(var_id, val, assignment)
            if consistent:
                # Pasang sementara waktu mulai aktivitas
                assignment[var_id] = val
                log_step("consistent", var_id, val, assignment, f"Berhasil menempatkan {act.name} pada pukul {val:02d}.00 (Konsisten)")
                
                # Rekursi ke variabel berikutnya
                result = backtrack(assignment)
                if result is not None:
                    return result
                
                # Jika langkah berikutnya gagal, lakukan backtrack (kembalikan status)
                del assignment[var_id]
                log_step("backtrack", var_id, val, assignment, f"Membatalkan {act.name} dari pukul {val:02d}.00 karena langkah berikutnya tidak menghasilkan solusi")
            else:
                # Log jika terjadi pelanggaran batasan
                log_step("conflict", var_id, val, assignment, f"Gagal menempatkan {act.name} pada pukul {val:02d}.00. Alasan: {reason}")
                
        return None

    # Jalankan pencarian backtracking
    initial_assignment = {}
    solution = backtrack(initial_assignment)
    
    final_schedule = None
    if solution:
        final_schedule = {h: "Kosong" for h in range(7, 22)}
        for var_id, start in solution.items():
            act = act_map[var_id]
            for h in range(start, start + act.duration):
                final_schedule[h] = act.name
        # Menggunakan id variabel pertama untuk logging sukses
        dummy_var = variables[0] if variables else "none"
        log_step("success", dummy_var, 0, solution, "Jadwal harian berhasil disusun dan bebas dari konflik!")
    else:
        dummy_var = variables[0] if variables else "none"
        log_step("fail", dummy_var, 0, {}, "Tidak ditemukan kombinasi jadwal yang memenuhi seluruh batasan!")
        
    return final_schedule, log_steps
