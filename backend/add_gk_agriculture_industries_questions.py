
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

LESSON_ID = 176
LESSON_TITLE = "Indian Agriculture, Industries, Transport and Infrastructure"
TOPIC = "General Knowledge"

BANK = {
    "Easy": [
        ("Which crop is known as the golden fibre of India?", "Jute", "Cotton", "Wheat", "Rice"),
        ("Which is the major food crop cultivated in India?", "Rice", "Tea", "Coffee", "Rubber"),
        ("Which season is associated with the cultivation of kharif crops?", "Monsoon", "Winter", "Summer only", "Spring"),
        ("Which season is associated with rabi crops?", "Winter", "Monsoon", "Autumn only", "Rainy season"),
        ("Which crop is commonly grown during the rabi season?", "Wheat", "Rice", "Cotton", "Jute"),
        ("Which crop requires high temperature and plenty of water?", "Rice", "Mustard", "Gram", "Barley"),
        ("Which Indian state is famous for tea production?", "Assam", "Rajasthan", "Punjab", "Haryana"),
        ("Which state is widely known for coffee cultivation in India?", "Karnataka", "Punjab", "Bihar", "Haryana"),
        ("Which crop is used to produce sugar?", "Sugarcane", "Cotton", "Jute", "Tea"),
        ("Which agricultural activity involves rearing silkworms?", "Sericulture", "Apiculture", "Pisciculture", "Horticulture"),
        ("What is the rearing of honeybees called?", "Apiculture", "Sericulture", "Pisciculture", "Viticulture"),
        ("What is the cultivation of fruits and vegetables called?", "Horticulture", "Sericulture", "Apiculture", "Dairy farming"),
        ("Which institution provides agricultural credit and supports rural development in India?", "NABARD", "SEBI", "ISRO", "FIFA"),
        ("Which organisation is responsible for promoting agricultural research in India?", "ICAR", "ISRO", "DRDO", "UGC"),
        ("What does MSP stand for in Indian agriculture?", "Minimum Support Price", "Maximum Selling Price", "Minimum Supply Product", "Market Support Programme"),
        ("Which crop is commonly associated with the Green Revolution in India?", "Wheat", "Tea", "Coffee", "Rubber"),
        ("Who is known as the father of the Green Revolution in India?", "M. S. Swaminathan", "Verghese Kurien", "Vikram Sarabhai", "Homi Bhabha"),
        ("Which revolution is associated with increased milk production in India?", "White Revolution", "Green Revolution", "Blue Revolution", "Yellow Revolution"),
        ("Who is known as the father of the White Revolution in India?", "Verghese Kurien", "M. S. Swaminathan", "Norman Borlaug", "C. Subramaniam"),
        ("Which mode of transport is most suitable for carrying heavy goods over long distances on land?", "Railways", "Bicycles", "Motorcycles", "Auto-rickshaws"),
        ("Which is the fastest mode of passenger transport over long distances?", "Airways", "Roadways", "Waterways", "Railways"),
        ("Which Indian city is known as the Silicon Valley of India?", "Bengaluru", "Mumbai", "Kolkata", "Jaipur"),
        ("Which industry is commonly called the backbone of modern industry?", "Iron and steel industry", "Toy industry", "Handicraft industry", "Food retail industry"),
        ("Which Indian city is famous for its textile industry and is often called the Manchester of India?", "Ahmedabad", "Delhi", "Patna", "Shimla"),
        ("Which port is located in Mumbai?", "Mumbai Port", "Paradip Port", "Kandla Port", "Haldia Port"),
        ("Which Indian state is famous for the major automobile manufacturing hub of Chennai?", "Tamil Nadu", "Punjab", "Assam", "Himachal Pradesh"),
        ("What is the main purpose of irrigation?", "Supply water to crops", "Harvest crops", "Store seeds", "Transport agricultural products"),
        ("Which of these is a natural fertiliser?", "Compost", "Plastic", "Petrol", "Diesel"),
        ("Which sector includes farming, fishing and forestry?", "Primary sector", "Secondary sector", "Tertiary sector", "Quaternary sector"),
        ("Which sector includes manufacturing and construction?", "Secondary sector", "Primary sector", "Tertiary sector", "Household sector"),
    ],

    "Medium": [
        ("Which Indian state is the largest producer of wheat among the following?", "Uttar Pradesh", "Kerala", "Goa", "Meghalaya"),
        ("Which state is a major producer of cotton in India?", "Gujarat", "Sikkim", "Manipur", "Himachal Pradesh"),
        ("Which crop is commonly called a plantation crop?", "Tea", "Wheat", "Gram", "Barley"),
        ("Which soil type is particularly suitable for cotton cultivation?", "Black soil", "Laterite soil", "Desert soil", "Mountain soil"),
        ("Which soil is commonly found in the Indo-Gangetic plains?", "Alluvial soil", "Black soil", "Laterite soil", "Mountain soil"),
        ("Which agricultural practice involves growing different crops in a planned sequence?", "Crop rotation", "Monoculture", "Deforestation", "Overgrazing"),
        ("What is mixed farming?", "Growing crops and rearing livestock together", "Growing only one crop", "Growing crops without irrigation", "Cultivating only fruits"),
        ("Which method of irrigation delivers water directly near plant roots?", "Drip irrigation", "Flood irrigation", "Canal flooding", "Traditional tank irrigation"),
        ("Which irrigation method sprays water over crops like rainfall?", "Sprinkler irrigation", "Drip irrigation", "Basin irrigation", "Furrow irrigation"),
        ("What is the main objective of crop insurance schemes?", "Protect farmers against specified crop losses", "Guarantee export profits", "Provide free machinery to every farmer", "Fix international crop prices"),
        ("Which scheme provides crop insurance to farmers in India?", "Pradhan Mantri Fasal Bima Yojana", "PM-KISAN", "Ujjwala Yojana", "Ayushman Bharat"),
        ("Which scheme provides income support to eligible farmer families?", "PM-KISAN", "PM-JAY", "PMAY", "Digital India"),
        ("Which institution is primarily responsible for agricultural research and education in India?", "Indian Council of Agricultural Research", "Reserve Bank of India", "SEBI", "NITI Aayog"),
        ("Which Indian agricultural scientist played a major role in developing high-yielding wheat varieties?", "M. S. Swaminathan", "C. V. Raman", "Vikram Sarabhai", "Verghese Kurien"),
        ("Which revolution is associated with increased fish production?", "Blue Revolution", "White Revolution", "Yellow Revolution", "Golden Revolution"),
        ("Which revolution is associated with increased oilseed production?", "Yellow Revolution", "Blue Revolution", "White Revolution", "Pink Revolution"),
        ("Which industry uses bauxite as its principal raw material?", "Aluminium industry", "Cement industry", "Paper industry", "Sugar industry"),
        ("Which mineral is the principal raw material for the iron and steel industry?", "Iron ore", "Mica", "Limestone only", "Gypsum"),
        ("Which industry is an example of an agro-based industry?", "Sugar industry", "Iron and steel industry", "Cement industry", "Aluminium industry"),
        ("Which industry is mainly based on forest products?", "Paper industry", "Petroleum refining", "Automobile industry", "Electronics industry"),
        ("Which Indian city is an important centre of the jute industry?", "Kolkata", "Jaipur", "Bengaluru", "Chandigarh"),
        ("Which Indian port is located in Odisha?", "Paradip Port", "Mumbai Port", "Mormugao Port", "Kochi Port"),
        ("Which port is located in Gujarat and was formerly known as Kandla Port?", "Deendayal Port", "Chennai Port", "Kochi Port", "Visakhapatnam Port"),
        ("Which organisation manages the national highways network in India?", "National Highways Authority of India", "RBI", "NABARD", "SEBI"),
        ("Which railway zone has its headquarters in Hubballi?", "South Western Railway", "Northern Railway", "Eastern Railway", "Western Railway"),
        ("Which transport mode is particularly useful for transporting bulky goods internationally at low cost?", "Waterways", "Airways", "Motorcycles", "Helicopters"),
        ("What is a major advantage of pipeline transport?", "Continuous transport of fluids and gases", "Suitable for transporting passengers", "Requires no infrastructure", "Best for transporting livestock"),
        ("Which Indian metro system was the first to begin operations?", "Kolkata Metro", "Delhi Metro", "Bengaluru Metro", "Chennai Metro"),
        ("Which sector provides services such as banking, transport and communication?", "Tertiary sector", "Primary sector", "Secondary sector", "Agricultural sector"),
        ("Which programme focuses on developing industrial corridors and manufacturing infrastructure in India?", "Make in India", "Beti Bachao Beti Padhao", "PM-KISAN", "Swachh Bharat Mission"),
    ],

    "Hard": [
        ("Which agricultural revolution in India is associated with increased horticultural production?", "Golden Revolution", "Blue Revolution", "White Revolution", "Grey Revolution"),
        ("Which Indian state is widely recognised for its high productivity in rice cultivation?", "Punjab", "Rajasthan", "Ladakh", "Haryana"),
        ("Which crop is commonly associated with black cotton soil and a warm climate?", "Cotton", "Tea", "Jute", "Apple"),
        ("Which agricultural practice involves cultivating crops without disturbing the soil through conventional ploughing?", "Zero tillage", "Shifting cultivation", "Terrace farming", "Monocropping"),
        ("What is precision agriculture?", "Using technology and data to optimise farm management", "Cultivating crops without seeds", "Growing only one crop every year", "Using only traditional tools"),
        ("Which technology is commonly used to monitor crop health over large areas?", "Remote sensing", "Typewriting", "Sound recording", "Manual bookkeeping"),
        ("Which organisation operates the e-NAM platform in India?", "Small Farmers' Agribusiness Consortium", "Reserve Bank of India", "SEBI", "Food Safety and Standards Authority of India"),
        ("What does e-NAM stand for?", "National Agriculture Market", "National Animal Management", "New Agricultural Machinery", "National Agro Manufacturing"),
        ("Which Indian body is responsible for food grain procurement and distribution under the public distribution system?", "Food Corporation of India", "NABARD", "SEBI", "NITI Aayog"),
        ("Which institution sets minimum support prices after considering recommendations from the Commission for Agricultural Costs and Prices?", "Government of India", "Reserve Bank of India", "Election Commission", "Supreme Court"),
        ("What is the main function of the Commission for Agricultural Costs and Prices?", "Recommend minimum support prices", "Regulate stock exchanges", "Manage railway operations", "Issue currency"),
        ("Which type of farming is characterised by growing crops mainly for household consumption?", "Subsistence farming", "Commercial farming", "Plantation farming", "Industrial farming"),
        ("Which farming system involves growing crops on cleared forest land for a limited period before moving elsewhere?", "Shifting cultivation", "Terrace farming", "Intensive farming", "Mixed farming"),
        ("Which Indian agricultural region is especially associated with tea plantations in the Brahmaputra Valley?", "Assam", "Punjab", "Rajasthan", "Gujarat"),
        ("Which industry is known for using limestone and clay as major raw materials?", "Cement industry", "Cotton textile industry", "Sugar industry", "Jute industry"),
        ("Which steel plant is located in Jharkhand?", "Bokaro Steel Plant", "Bhilai Steel Plant", "Rourkela Steel Plant", "Salem Steel Plant"),
        ("Which steel plant is located in Odisha?", "Rourkela Steel Plant", "Bhilai Steel Plant", "Bokaro Steel Plant", "Durgapur Steel Plant"),
        ("Which steel plant is located in Chhattisgarh?", "Bhilai Steel Plant", "Rourkela Steel Plant", "Bokaro Steel Plant", "Visvesvaraya Iron and Steel Plant"),
        ("Which public sector company operates major oil refineries and petroleum infrastructure in India?", "Indian Oil Corporation", "NABARD", "BHEL", "HAL"),
        ("Which Indian company is strongly associated with the development of the private-sector automobile industry?", "Tata Motors", "NABARD", "SEBI", "GAIL"),
        ("Which industrial corridor connects Mumbai and Delhi?", "Delhi-Mumbai Industrial Corridor", "Chennai-Bengaluru Industrial Corridor", "Amritsar-Kolkata Industrial Corridor", "East Coast Economic Corridor"),
        ("Which Indian port is a major natural harbour on the west coast of India?", "Mumbai Port", "Haldia Port", "Paradip Port", "Kolkata Port"),
        ("Which port is located on the eastern coast of India in Andhra Pradesh?", "Visakhapatnam Port", "Mormugao Port", "Kandla Port", "New Mangalore Port"),
        ("Which Indian inland waterway connects Prayagraj and Haldia?", "National Waterway 1", "National Waterway 2", "National Waterway 3", "National Waterway 4"),
        ("Which National Waterway is located along the Brahmaputra River?", "National Waterway 2", "National Waterway 1", "National Waterway 3", "National Waterway 5"),
        ("Which organisation is responsible for the development and regulation of civil aviation in India?", "Directorate General of Civil Aviation", "NABARD", "SEBI", "CPCB"),
        ("Which organisation operates major airports in India under government ownership?", "Airports Authority of India", "Food Corporation of India", "National Highways Authority of India", "Railway Board"),
        ("Which dedicated freight corridor is designed to connect Ludhiana with Dankuni?", "Eastern Dedicated Freight Corridor", "Western Dedicated Freight Corridor", "Konkan Railway", "Golden Quadrilateral"),
        ("Which national highway development programme connects Delhi, Mumbai, Chennai and Kolkata?", "Golden Quadrilateral", "North-South Corridor only", "East-West Corridor only", "Bharatmala only"),
        ("Which scheme focuses on improving rural road connectivity in India?", "Pradhan Mantri Gram Sadak Yojana", "PM-KISAN", "PM-JAY", "Ujjwala Yojana"),
    ]
}


def validate_bank():
    for difficulty, questions in BANK.items():
        if len(questions) != 30:
            raise ValueError(
                f"{difficulty}: Expected 30 questions, found {len(questions)}"
            )

        for index, item in enumerate(questions, 1):
            if len(item) != 5:
                raise ValueError(
                    f"Invalid question format: {difficulty} #{index}"
                )

            question, correct, *wrong = item
            options = [correct] + wrong

            if not all(isinstance(value, str) and value.strip() for value in item):
                raise ValueError(
                    f"Empty field: {difficulty} #{index}"
                )

            if len(set(options)) != 4:
                raise ValueError(
                    f"Duplicate options: {difficulty} #{index}"
                )

    print("Question bank validation successful.")


def main():
    validate_bank()

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT title, topic FROM lessons WHERE id = ?",
            (LESSON_ID,)
        )
        existing = cursor.fetchone()

        if existing is None:
            cursor.execute("""
                INSERT INTO lessons
                (id, title, topic, difficulty, content, created_at)
                VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (
                LESSON_ID,
                LESSON_TITLE,
                TOPIC,
                "Mixed",
                "Learn about Indian agriculture, crop seasons, agricultural revolutions, industries, transport systems and infrastructure."
            ))

        elif existing != (LESSON_TITLE, TOPIC):
            raise ValueError(
                f"Lesson ID {LESSON_ID} is already occupied by {existing}"
            )

        for difficulty, questions in BANK.items():
            cursor.execute("""
                SELECT id FROM quizzes
                WHERE lesson_id = ? AND difficulty = ?
            """, (LESSON_ID, difficulty))

            quiz_rows = cursor.fetchall()

            if len(quiz_rows) > 1:
                raise ValueError(
                    f"Multiple {difficulty} quizzes found."
                )

            if quiz_rows:
                quiz_id = quiz_rows[0][0]
            else:
                cursor.execute("""
                    INSERT INTO quizzes (lesson_id, title, difficulty)
                    VALUES (?, ?, ?)
                """, (
                    LESSON_ID,
                    f"{LESSON_TITLE} - {difficulty}",
                    difficulty
                ))
                quiz_id = cursor.lastrowid

            cursor.execute(
                "SELECT COUNT(*) FROM questions WHERE quiz_id = ?",
                (quiz_id,)
            )
            existing_count = cursor.fetchone()[0]

            if existing_count > 30:
                raise ValueError(
                    f"{difficulty} already has {existing_count} questions."
                )

            for item in questions[existing_count:]:
                question, correct, wrong1, wrong2, wrong3 = item

                options = [correct, wrong1, wrong2, wrong3]
                random.shuffle(options)

                correct_letter = "ABCD"[options.index(correct)]

                cursor.execute("""
                    INSERT INTO questions (
                        quiz_id, question,
                        option_a, option_b, option_c, option_d,
                        correct_answer
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    quiz_id,
                    question,
                    options[0],
                    options[1],
                    options[2],
                    options[3],
                    correct_letter
                ))

            cursor.execute(
                "SELECT COUNT(*) FROM questions WHERE quiz_id = ?",
                (quiz_id,)
            )
            final_count = cursor.fetchone()[0]

            if final_count != 30:
                raise ValueError(
                    f"{difficulty} has {final_count} questions instead of 30."
                )

            print(f"{difficulty}: {final_count}/30 SUCCESS")

        connection.commit()

        print("\n====================================")
        print("GK TOPIC 16 INSERTED SUCCESSFULLY")
        print("Indian Agriculture, Industries, Transport and Infrastructure")
        print("Easy: 30")
        print("Medium: 30")
        print("Hard: 30")
        print("TOTAL: 90 QUESTIONS")
        print("====================================")

    except Exception as error:
        connection.rollback()
        print("ERROR:", error)
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    main()
