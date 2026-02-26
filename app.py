import os
import subprocess
import xml.etree.ElementTree as ET
import customtkinter as ctk
import sys
import threading
import tkinter.messagebox

ctk.set_appearance_mode("System")  
ctk.set_default_color_theme("blue")

VERSION = "v1.2.0"
APP_NAME = "Salud de Batería Windows"

class BatteryHealthApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(f"{APP_NAME} {VERSION}")
        # Agrandamos la ventana para acomodar la nueva información de forma limpia
        self.geometry("500x650")
        self.minsize(500, 650)
        
        try:
            # Icono proporcionado por el usuario
            self.iconbitmap("D:/Mis cosas/Utilidad Battery Report/battery.ico")
        except:
            pass

        # Grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Header
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        self.header_frame.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(self.header_frame, text="Reporte de Salud de Batería de Windows", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.grid(row=0, column=0, sticky="w")
        
        self.subtitle_label = ctk.CTkLabel(self.header_frame, text="Analiza la salud de tu batería con el sistema nativo.", font=ctk.CTkFont(size=12), text_color="gray")
        self.subtitle_label.grid(row=1, column=0, sticky="w", pady=(2, 0))

        # Botón de Información Modificado
        self.info_button = ctk.CTkButton(
            self.header_frame, 
            text="ℹ Info", 
            width=60, 
            command=self.show_info,
            fg_color="transparent",
            border_width=1,
            text_color=("black", "white")
        )
        self.info_button.grid(row=0, column=1, rowspan=2, sticky="e")

        # Scrollable Content Frame para no saturar la vista estática
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        self.scroll_frame.grid_columnconfigure(0, weight=1)

        # --- SECCIÓN PRINCIPAL (Jerarquía Superior) ---
        self.main_info_frame = ctk.CTkFrame(self.scroll_frame)
        self.main_info_frame.grid(row=0, column=0, pady=(0, 10), padx=10, sticky="ew")
        self.main_info_frame.grid_columnconfigure(1, weight=1)

        main_title = ctk.CTkLabel(self.main_info_frame, text="Estado General de la Batería", font=ctk.CTkFont(size=16, weight="bold"))
        main_title.grid(row=0, column=0, columnspan=2, padx=15, pady=(15, 10), sticky="w")

        # Datos prioritarios
        self.health_label = self._create_data_row(self.main_info_frame, "Salud Actual:", "---", 1)
        self.cycles_label = self._create_data_row(self.main_info_frame, "Ciclos de Carga:", "---", 2)
        self.design_label = self._create_data_row(self.main_info_frame, "Capacidad de Diseño:", "---", 3)
        self.full_label = self._create_data_row(self.main_info_frame, "Carga Máxima:", "---", 4)
        self.reduction_label = self._create_data_row(self.main_info_frame, "Desgaste Total:", "---", 5, font_weight="bold")
        
        # Barra de progreso
        self.health_progress = ctk.CTkProgressBar(self.main_info_frame, height=20)
        self.health_progress.grid(row=6, column=0, columnspan=2, padx=20, pady=(15, 20), sticky="ew")
        self.health_progress.set(0)


        # --- SECCIÓN DETALLADA (Jerarquía Inferior) ---
        self.extra_info_frame = ctk.CTkFrame(self.scroll_frame)
        self.extra_info_frame.grid(row=1, column=0, pady=10, padx=10, sticky="ew")
        self.extra_info_frame.grid_columnconfigure(1, weight=1)

        extra_title = ctk.CTkLabel(self.extra_info_frame, text="Información Detallada (Avanzada)", font=ctk.CTkFont(size=14, weight="bold"), text_color="gray")
        extra_title.grid(row=0, column=0, columnspan=2, padx=15, pady=(15, 10), sticky="w")

        # Datos de hardware
        self.computer_name_label = self._create_data_row(self.extra_info_frame, "Nombre del Equipo:", "---", 1, size=12)
        self.computer_model_label = self._create_data_row(self.extra_info_frame, "Modelo del Equipo:", "---", 2, size=12)
        self.computer_year_label = self._create_data_row(self.extra_info_frame, "Año Fabricación / BIOS:", "---", 3, size=12)
        
        # Agregamos una separación sutil
        separator = ctk.CTkFrame(self.extra_info_frame, height=2, fg_color=("gray75", "gray25"))
        separator.grid(row=4, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

        # Datos extra de batería y sistema
        self.battery_model_label = self._create_data_row(self.extra_info_frame, "Modelo de Batería:", "---", 5, size=12)
        self.battery_manufacturer_label = self._create_data_row(self.extra_info_frame, "Fabricante Batería:", "---", 6, size=12)
        self.battery_chemistry_label = self._create_data_row(self.extra_info_frame, "Química de Batería:", "---", 7, size=12)
        self.battery_year_label = self._create_data_row(self.extra_info_frame, "Año Fab. Batería:", "---", 8, size=12)
        self.os_build_label = self._create_data_row(self.extra_info_frame, "Build del Sistema (SO):", "---", 9, size=12)
        
        self.extra_info_frame.grid_rowconfigure(10, minsize=10) # Padding inferior


        # --- BOTONES Y FOOTER ---
        self.bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.bottom_frame.grid(row=2, column=0, padx=20, pady=(10, 20), sticky="s")

        self.refresh_button = ctk.CTkButton(
            self.bottom_frame, 
            text="Generar Reporte", 
            font=ctk.CTkFont(size=15, weight="bold"), 
            height=40,
            command=self.generate_and_load_report
        )
        self.refresh_button.pack()
        
        self.status_label = ctk.CTkLabel(self.bottom_frame, text="Listo.", font=ctk.CTkFont(size=11), text_color="gray")
        self.status_label.pack(pady=(5, 0))

        # Cargar inicial
        if os.path.exists("battery_report.xml"):
            self.load_report_data()

    def show_info(self):
        # Modal con información del autor y versión
        info_text = (
            f"{APP_NAME}\n"
            f"Versión: {VERSION}\n\n"
            f"Autor: Firo\n"
            f"Email: firogv96@outlook.com"
        )
        tkinter.messagebox.showinfo("Acerca de", info_text)

    def _create_data_row(self, parent_frame, title, initial_val, row_idx, size=14, font_weight="normal"):
        title_lbl = ctk.CTkLabel(parent_frame, text=title, font=ctk.CTkFont(size=size, weight=font_weight))
        title_lbl.grid(row=row_idx, column=0, padx=(20, 10), pady=4, sticky="w")
        
        val_lbl = ctk.CTkLabel(parent_frame, text=initial_val, font=ctk.CTkFont(size=size))
        val_lbl.grid(row=row_idx, column=1, padx=(10, 20), pady=4, sticky="e")
        return val_lbl

    def generate_and_load_report(self):
        self.status_label.configure(text="Generando reporte de Windows...")
        self.refresh_button.configure(state="disabled")
        self.update_idletasks()

        def task():
            try:
                subprocess.run(
                    ["powercfg", "/batteryreport", "/xml", "-OUTPUT", "battery_report.xml"],
                    creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
                    check=True
                )
                self.after(100, self.load_report_data)
            except Exception as e:
                self.after(100, lambda: self._show_error(f"Error al generar reporte: {e}"))
                
        threading.Thread(target=task, daemon=True).start()

    def _show_error(self, message):
        self.status_label.configure(text=message, text_color="red")
        self.refresh_button.configure(state="normal")

    def load_report_data(self):
        try:
            if not os.path.exists("battery_report.xml"):
                self.status_label.configure(text="No se encontró el reporte previo. Genera uno nuevo.")
                self.refresh_button.configure(state="normal")
                return

            tree = ET.parse("battery_report.xml")
            root = tree.getroot()

            ns = {'batt': 'http://schemas.microsoft.com/battery/2012'}
            
            # --- 1. PROCESAR INFORMACIÓN DEL SISTEMA ---
            sys_info = root.find('.//batt:SystemInformation', ns)
            if sys_info is not None:
                c_name = sys_info.find('batt:ComputerName', ns)
                c_manuf = sys_info.find('batt:SystemManufacturer', ns)
                c_prod = sys_info.find('batt:SystemProductName', ns)
                bios_date = sys_info.find('batt:BIOSDate', ns)
                os_build = sys_info.find('batt:OSBuild', ns)

                str_c_name = c_name.text if c_name is not None and c_name.text else "Desconocido"
                str_c_manuf = c_manuf.text if c_manuf is not None and c_manuf.text else ""
                str_c_prod = c_prod.text if c_prod is not None and c_prod.text else "Desconocido"
                
                model_full = f"{str_c_manuf} {str_c_prod}".strip()
                
                self.computer_name_label.configure(text=str_c_name)
                self.computer_model_label.configure(text=model_full if model_full else "Desconocido")
                
                # Tratar de parsear el año desde la BIOS (ej: 11/26/2025)
                str_bios = bios_date.text if bios_date is not None and bios_date.text else "Desconocido"
                try:
                    if "/" in str_bios:
                        year = str_bios.split("/")[-1]
                        str_bios = f"{str_bios} (Año aprox: {year})"
                except:
                    pass
                self.computer_year_label.configure(text=str_bios)
                
                self.os_build_label.configure(text=os_build.text if os_build is not None and os_build.text else "Desconocido")


            # --- 2. PROCESAR INFORMACIÓN DE BATERÍAS ---
            design_capacity_total = 0
            full_charge_capacity_total = 0
            cycle_count_total = 0

            batteries = root.findall('.//batt:Batteries/batt:Battery', ns)
            
            if not batteries:
                self._show_error("No se encontraron datos de batería en el reporte.")
                return

            # Para la info avanzada, tomamos la primer batería
            first_batt = batteries[0]
            b_id = first_batt.find('batt:Id', ns)
            b_manuf = first_batt.find('batt:Manufacturer', ns)
            b_chem = first_batt.find('batt:Chemistry', ns)
            b_date = first_batt.find('batt:ManufactureDate', ns)

            b_id_str = b_id.text if b_id is not None and b_id.text else "Desconocido"
            self.battery_model_label.configure(text=b_id_str)
            
            b_man_str = b_manuf.text if b_manuf is not None and b_manuf.text else "Desconocido"
            self.battery_manufacturer_label.configure(text=b_man_str)
            
            # Formatear la Química a algo más legible
            chem_str = b_chem.text if b_chem is not None and b_chem.text else ""
            if chem_str == "LiP":
                chem_str = "LiP (Polímero de Litio)"
            elif chem_str == "LION":
                chem_str = "LION (Iones de Litio)"
            elif not chem_str:
                chem_str = "Desconocido"
            self.battery_chemistry_label.configure(text=chem_str)
            
            # Fecha de la batería
            b_date_str = b_date.text if b_date is not None and b_date.text else "No registrada en OS"
            self.battery_year_label.configure(text=b_date_str)


            # Acumular sumas por si la computadora tiene 2 o más baterías (ej. laptops profesionales)
            for battery in batteries:
                dc_str = battery.find('batt:DesignCapacity', ns)
                fcc_str = battery.find('batt:FullChargeCapacity', ns)
                cc_str = battery.find('batt:CycleCount', ns)
                
                if dc_str is not None and dc_str.text:
                    design_capacity_total += int(dc_str.text)
                if fcc_str is not None and fcc_str.text:
                    full_charge_capacity_total += int(fcc_str.text)
                if cc_str is not None and cc_str.text and cc_str.text != '-':
                    cycle_count_total += int(cc_str.text)

            if design_capacity_total == 0:
                self._show_error("Capacidad de diseño inválida.")
                return

            # Cálculos core
            health_percent = (full_charge_capacity_total / design_capacity_total) * 100
            reduction = design_capacity_total - full_charge_capacity_total

            self.design_label.configure(text=f"{design_capacity_total:,} mWh")
            self.full_label.configure(text=f"{full_charge_capacity_total:,} mWh")
            
            if reduction > 0:
                self.reduction_label.configure(text=f"{reduction:,} mWh", text_color="orange")
            else:
                self.reduction_label.configure(text="0 mWh (Batería nueva / 100%)", text_color="green")
                
            self.cycles_label.configure(text=str(cycle_count_total))
            
            # UI lógica de colores para salud
            if health_percent >= 80:
                health_color = "green"
                progress_color = ["#2ecc71", "#27ae60"]
            elif health_percent >= 50:
                health_color = "orange"
                progress_color = ["#e67e22", "#d35400"]
            else:
                health_color = "red"
                progress_color = ["#e74c3c", "#c0392b"]

            self.health_label.configure(text=f"{health_percent:.1f} %", text_color=health_color)
            self.health_progress.set(health_percent / 100.0)
            self.health_progress.configure(progress_color=progress_color)

            self.status_label.configure(text=f"Reporte cargado exitosamente.", text_color="gray")

        except Exception as e:
            self._show_error(f"Error al analizar el reporte: {e}")
        finally:
            self.refresh_button.configure(state="normal")

if __name__ == "__main__":
    app = BatteryHealthApp()
    app.mainloop()
