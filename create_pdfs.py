from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

styles = getSampleStyleSheet()

def create_pdf(filename, title, sections):
    doc = SimpleDocTemplate(filename, pagesize=A4)
    content = []
    content.append(Paragraph(title, styles['Title']))
    content.append(Spacer(1, 20))
    for heading, text in sections:
        content.append(Paragraph(heading, styles['Heading1']))
        content.append(Paragraph(text, styles['Normal']))
        content.append(Spacer(1, 12))
    doc.build(content)
    print(f"✅ {filename} créé !")

create_pdf("data/manuel_rh.pdf", "Manuel des Ressources Humaines", [
    ("1. Congés payés", "Chaque employé bénéficie de 25 jours de congés payés par an. Les congés doivent être demandés au moins 2 semaines à l'avance via l'outil RH interne. Les congés non pris avant le 31 décembre sont perdus sauf accord exceptionnel du manager."),
    ("2. Onboarding", "Tout nouvel employé suit une période d'intégration de 4 semaines. La première semaine est dédiée à la découverte de l'entreprise et des outils. Un mentor est assigné à chaque nouveau collaborateur pour l'accompagner pendant 3 mois."),
    ("3. Télétravail", "Le télétravail est autorisé jusqu'à 3 jours par semaine. L'employé doit être joignable pendant les heures de travail habituelles (9h-18h). Un accord de télétravail doit être signé avec le manager avant de commencer."),
    ("4. Congé maternité et paternité", "Le congé maternité est de 16 semaines minimum selon la législation française. Le congé paternité est de 25 jours calendaires. Ces congés sont intégralement rémunérés par l'entreprise au-delà des indemnités légales."),
    ("5. Formation", "Chaque employé dispose d'un budget formation annuel de 1500 euros. Les demandes de formation doivent être validées par le manager et les RH. Les formations peuvent être suivies en présentiel ou en ligne.")
])

create_pdf("data/guide_securite.pdf", "Guide de Sécurité Informatique", [
    ("1. Mots de passe", "Les mots de passe doivent contenir au minimum 12 caractères, une majuscule, un chiffre et un caractère spécial. Ils doivent être changés tous les 90 jours. Il est strictement interdit de partager son mot de passe avec un collègue."),
    ("2. Signalement d'incident", "Tout incident de sécurité doit être signalé immédiatement à security@entreprise.com. Un incident peut être : un email suspect, un accès non autorisé, une perte de matériel. Le délai maximum de signalement est de 2 heures après détection."),
    ("3. Utilisation des appareils", "Les appareils professionnels ne doivent pas être utilisés à des fins personnelles. L'installation de logiciels non approuvés est interdite. En cas de perte ou vol, contacter immédiatement le service IT au +33 1 23 45 67 89."),
    ("4. Données confidentielles", "Les données clients sont classifiées CONFIDENTIEL et ne doivent jamais être partagées en dehors de l'entreprise. L'envoi de données sensibles par email personnel est strictement interdit. Toutes les données doivent être stockées sur les serveurs approuvés."),
    ("5. Télétravail et sécurité", "En télétravail, l'utilisation du VPN est obligatoire. Les réseaux WiFi publics sont interdits sans VPN actif. L'écran doit être verrouillé dès que vous quittez votre poste de travail.")
])

create_pdf("data/reglement_interne.pdf", "Règlement Intérieur de l'Entreprise", [
    ("1. Horaires de travail", "Les horaires de travail sont de 9h à 18h du lundi au vendredi. Une pause déjeuner d'une heure est obligatoire entre 12h et 14h. Des horaires flexibles peuvent être accordés sur demande au manager avec un plage fixe obligatoire de 10h à 16h."),
    ("2. Dress code", "La tenue vestimentaire doit être professionnelle et soignée. Le port de shorts, tongs ou vêtements à slogans est interdit dans les locaux. Les vendredis sont casual, une tenue décontractée mais correcte est acceptée."),
    ("3. Espaces communs", "Les espaces communs doivent être laissés propres après utilisation. La cuisine est accessible de 7h à 20h. Les réunions dans les salles doivent être réservées via l'outil de réservation en ligne au moins 1 heure à l'avance."),
    ("4. Politique anti-discrimination", "L'entreprise applique une politique stricte de tolérance zéro face à toute forme de discrimination. Tout comportement discriminatoire doit être signalé aux RH immédiatement. Une enquête interne sera ouverte dans les 48h suivant tout signalement."),
    ("5. Utilisation du matériel", "Le matériel mis à disposition est sous la responsabilité de l'employé. Toute casse ou perte doit être signalée sous 24h au service IT. Le matériel doit être restitué en bon état lors de la fin du contrat.")
])