import smtplib
import streamlit as st
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import plotly.express as px
import numpy as np
import pandas as pd
from io import BytesIO

def send_email(subject, body, to_email, from_email, from_password, image_data=None):
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach email body text
    msg.attach(MIMEText(body, 'html'))

    # Attach image if available
    if image_data:
        image = MIMEImage(image_data, name="graph.png")
        msg.attach(image)

    try:
        # Connect to Gmail SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Start TLS encryption
            server.login(from_email, from_password)  # Login with email and app-specific password
            server.send_message(msg)  # Send the email
        print("Email envoyé avec succès!")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email: {e}")

def create_plot():
    # Example data
    df = pd.DataFrame({
        'date': pd.date_range(start='2024-01-01', periods=10, freq='D'),
        'PO43-  (mg/l)': np.random.randn(10)
    })

    # Streamlit display
    st.markdown(f"<h2 style='text-align: center;'>PO43- (mg/l) moyenne: {np.around(df['PO43-  (mg/l)'].mean(),2)} mg/l</h2>", unsafe_allow_html=True)
    fig = px.line(df, x="date", y="PO43-  (mg/l)")
    fig.add_hline(y=0, line_dash="dash", line_color="red", line_width=2)
    fig.add_annotation(
        x=df['date'].iloc[-1],
        y=0,
        text="PO43- doit être égale à 0",
        showarrow=True,
        arrowhead=2,
        ax=0,
        ay=-40
    )
    st.plotly_chart(fig, use_container_width=True, height=200)
    
    # Convert figure to image bytes
    img_bytes = fig.to_image(format="png")
    return img_bytes, df

def check_and_notify(from_email, from_password):
    plot_img, df = create_plot()
    if df['PO43-  (mg/l)'].iloc[-1] != 0:  # Check if the last value is not 0
        email_body = "<h1>Notification de Graphique</h1><p>La valeur de PO43- (mg/l) est différente de 0. Voici le graphique avec l'annotation.</p>"
        send_email(
            subject="Alerte PO43- Différente de 0",
            body=email_body,
            to_email="aitomar.mip.97@gmail.com",
            from_email=from_email,
            from_password=from_password,
            image_data=plot_img
        )

if __name__ == "__main__":
    # Replace these values with your actual email and app-specific password
    from_email = "mohamed.aitomar@dips.ma"
    from_password = "ma&20242024"  # Mot de passe spécifique d'application
    check_and_notify(from_email, from_password)
