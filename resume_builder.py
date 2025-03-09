import streamlit as st
from fpdf import FPDF
import os
from PIL import Image

# ---- PAGE CONFIG ----
st.set_page_config(page_title="Resume Builder", page_icon="📄", layout="centered")

# ---- HEADER ----
st.title("📄 Resume Builder")
st.write("Fill in the details below and generate your resume as a PDF!")

# ---- USER INPUT FORM ----
with st.form("resume_form"):
    name = st.text_input("👤 Full Name")
    email = st.text_input("📧 Email")
    phone = st.text_input("📞 Phone Number")
    linkedin = st.text_input("🔗 LinkedIn URL")

    st.subheader("🎓 Education")
    education = st.text_area("Enter your education details")

    st.subheader("💼 Experience")
    experience = st.text_area("Enter your work experience details")

    st.subheader("🛠 Skills")
    skills = st.text_area("Enter your skills (comma-separated)")

    st.subheader("📸 Upload Image")
    image = st.file_uploader("Upload your profile picture", type=["jpg", "png"])

    submit = st.form_submit_button("Generate Resume")

# ---- PDF GENERATION FUNCTION ----
def create_pdf(name, email, phone, linkedin, education, experience, skills, image):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Adding Profile Image (Fixing RGBA issue)
    if image is not None:
        img = Image.open(image)

        # Convert RGBA to RGB (Fix Transparency Issue)
        if img.mode == "RGBA":
            img = img.convert("RGB")

        img_path = "profile.jpg"
        img.save(img_path, format="JPEG")  # Save as JPEG after conversion
        pdf.image(img_path, x=80, y=10, w=50, h=50)  # Adjust position and size
        os.remove(img_path)  # Delete after use

    pdf.set_font("Arial", "B", 16)
    pdf.ln(60)  # Adjust for image space
    pdf.cell(200, 10, name.encode("latin-1", "replace").decode("latin-1"), ln=True, align='C')

    pdf.set_font("Arial", "", 12)
    pdf.cell(200, 10, f"Email: {email} | Phone: {phone}", ln=True, align='C')
    pdf.cell(200, 10, f"LinkedIn: {linkedin}", ln=True, align='C')

    pdf.ln(10)  # Space

    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Education", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, education.encode("latin-1", "replace").decode("latin-1"))

    pdf.ln(5)

    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Experience", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, experience.encode("latin-1", "replace").decode("latin-1"))

    pdf.ln(5)

    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Skills", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, skills.replace(",", ", ").encode("latin-1", "replace").decode("latin-1"))

    return pdf

# ---- GENERATE & DOWNLOAD RESUME ----
if submit:
    if name and email and phone:
        pdf = create_pdf(name, email, phone, linkedin, education, experience, skills, image)
        pdf.output("resume.pdf", "F")  # Ensure it's written properly
        st.success("🎉 Resume generated successfully!")

        with open("resume.pdf", "rb") as pdf_file:
            st.download_button("📥 Download Resume", data=pdf_file, file_name="Resume.pdf", mime="application/pdf")
    else:
        st.error("⚠️ Please fill in all required fields!")
