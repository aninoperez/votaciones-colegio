import io
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Votación Nuevo Nombre del Colegio", page_icon="🗳️", layout="centered"
)

# --- CONFIGURACIÓN INICIAL DE ESTADOS ---
if "votos" not in st.session_state:
  st.session_state.votos = {
      "Candidata Aurora": 0,
      "Candidata Atenea": 0,
      "Candidata Milenio": 0,
      "Candidata Futuro": 0,
      "Candidata Sabiduría": 0,
  }

if "total_participantes" not in st.session_state:
  st.session_state.total_participantes = 0

TOTAL_ESTUDIANTES_META = 450

# --- TÍTULO Y PRESENTACIÓN ---
st.title("🗳️ Elección del Nuevo Nombre del Colegio")
st.write(
    "Selecciona tu opción favorita de manera libre y secreta. ¡Haz clic en"
    " votar para registrar tu opinión!"
)

tab1, tab2 = st.tabs(["🎓 Zona de Votación (Estudiantes)", "🔒 Panel Docente"])

# --- TAB 1: ZONA DE ESTUDIANTES ---
with tab1:
  st.subheader("Elige la nueva identidad del colegio")

  # Información de las candidatas (puedes cambiar los nombres o las fotos)
  candidatas_info = {
      "Candidata Aurora": (
          "Representa un nuevo comienzo.",
          "https://images.unsplash.com/photo-1580582932707-520aed937b7b?w=300",
      ),
      "Candidata Atenea": (
          "Símbolo de sabiduría e historia.",
          "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=300",
      ),
      "Candidata Milenio": (
          "Mirada hacia la modernidad y el futuro.",
          "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=300",
      ),
      "Candidata Futuro": (
          "Innovación y liderazgo estudiantil.",
          "https://images.unsplash.com/photo-1509062522246-3755977927d7?w=300",
      ),
      "Candidata Sabiduría": (
          "Tradición y excelencia académica.",
          "https://images.unsplash.com/photo-1427504494785-3a9ca7044f45?w=300",
      ),
  }

  opcion_elegida = st.radio(
      "Selecciona una de las opciones:", list(candidatas_info.keys())
  )

  # Mostrar la foto y descripción de la opción seleccionada
  desc, foto_url = candidatas_info[opcion_elegida]
  st.image(foto_url, width=300, caption=opcion_elegida)
  st.info(f"💡 **Propuesta:** {desc}")

  st.divider()

  # Botón para emitir el voto de forma directa
  if st.button("Confirmar y Registrar Mi Voto 🗳️️", type="primary"):
    st.session_state.votos[opcion_elegida] += 1
    st.session_state.total_participantes += 1
    st.success(
        "¡Voto registrado con éxito! Gracias, ya puedes pasar al siguiente"
        " estudiante."
    )
    st.balloons()
    # Opcional: recarga rápida para limpiar la pantalla para el siguiente alumno
    st.rerun()

# --- TAB 2: PANEL DE ADMINISTRACIÓN ---
with tab2:
  st.subheader("Panel de Control (Docentes)")
  password = st.text_input(
      "Contraseña de Administrador:", type="password", key="pass_admin"
  )

  if password == "colegio2026":
    st.success("Acceso de administrador concedido.")

    total_votos_emitidos = st.session_state.total_participantes
    porcentaje_participacion = (
        total_votos_emitidos / TOTAL_ESTUDIANTES_META
    ) * 100

    col1, col2 = st.columns(2)
    col1.metric(
        "Votos Totales", f"{total_votos_emitidos} / {TOTAL_ESTUDIANTES_META}"
    )
    col2.metric("Participación", f"{porcentaje_participacion:.2f}%")

    st.divider()
    st.markdown("### 📊 Resultados y Ranking")

    df_res = pd.DataFrame(
        list(st.session_state.votos.items()), columns=["Candidata", "Votos"]
    )
    df_res = df_res.sort_values(by="Votos", ascending=False).reset_index(
        drop=True
    )
    df_res["Ranking"] = [f"#{i+1}" for i in range(len(df_res))]

    st.dataframe(df_res[["Ranking", "Candidata", "Votos"]], use_container_width=True)

    fig = px.bar(
        df_res,
        x="Candidata",
        y="Votos",
        color="Candidata",
        title="Votación por Nombre",
        text="Votos",
    )
    st.plotly_chart(fig, use_container_width=True)

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
      df_res.to_excel(writer, index=False, sheet_name="Resultados_Votacion")
    excel_data = output.getvalue()

    st.download_button(
        label="📥 Descargar Resultados en Excel",
        data=excel_data,
        file_name="resultados_votacion_colegio.xlsx",
        mime=(
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ),
    )

  elif password:
    st.error("Contraseña incorrecta.")
