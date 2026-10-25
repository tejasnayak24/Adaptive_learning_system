import os
import random
import logging
from pathlib import Path

logging.disable(logging.CRITICAL)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "adaptive_learning.db"
os.environ["DATABASE_URL"] = f"sqlite:///{DATABASE_PATH.as_posix()}"

from app.database.connection import SessionLocal
from app.models.student import Student
from app.models.lesson import Lesson
from app.models.quiz import Quiz
from app.models.question import Question
from app.models.progress import Progress
from app.models.session import LearningSession
from app.models.reward import RewardHistory


QUESTION_BANK = {
    "Easy": [
        ("What is a market?", "A place or system where buyers and sellers exchange goods or services", "A place used only for sleeping", "A school examination", "A government office only", "A"),
        ("Who is a consumer?", "A person who buys or uses goods and services", "A person who only manufactures goods", "A person who collects taxes", "A person who builds roads", "A"),
        ("Who is a seller?", "A person who offers goods or services for sale", "A person who only buys goods", "A school student taking an exam", "A person who issues passports", "A"),
        ("What is a weekly market?", "A market held on a particular day each week", "A market that opens only once in ten years", "A permanent court", "A school library", "A"),
        ("Which is an example of a shop in a neighbourhood market?", "A grocery shop", "A railway signal room", "A courtroom", "A weather station", "A"),
        ("What does a wholesaler generally do?", "Sells goods in large quantities to retailers", "Buys only one item for personal use", "Runs a school examination", "Provides court judgments", "A"),
        ("Who is a retailer?", "A seller who commonly sells goods directly to consumers", "A person who only grows forests", "A person who makes laws", "A person who collects rainfall data", "A"),
        ("What is a commodity?", "A good that can be bought or sold", "A school timetable", "A court procedure", "A weather forecast", "A"),
        ("What is barter?", "Exchanging goods or services without using money", "Borrowing a book from a library", "Paying only with a bank card", "Depositing money in a bank", "A"),
        ("Why do people compare prices?", "To understand the cost of similar goods before buying", "To stop all trade", "To avoid checking product quality", "To make goods disappear", "A"),
        ("What is a shopping mall?", "A building or complex containing multiple shops and services", "A type of village council", "A farming tool", "A public court", "A"),
        ("Which is an example of an online market?", "A website where buyers can order products", "A classroom noticeboard", "A public garden", "A bus stop without shops", "A"),
        ("What is a producer?", "A person or organisation that makes or grows goods", "A person who only consumes products", "A person who only watches television", "A person who issues driving licences", "A"),
        ("What is a service?", "An activity performed to meet a need", "Only a physical object", "A type of currency note", "A shop building", "A"),
        ("What does a price tell a buyer?", "How much money is required to buy a product", "The buyer's school grade", "The weather in a city", "The distance to a mountain", "A"),
        ("Which factor can influence the price of a product?", "Demand and supply", "The colour of the shop wall only", "The buyer's handwriting", "The day of a school exam only", "A"),
        ("Why do people visit a local market?", "To buy goods and services they need", "To conduct every court case", "To issue passports", "To elect judges directly", "A"),
        ("What is a transaction?", "An exchange involving goods, services, or payment", "A school holiday", "A type of mountain", "A weather condition", "A"),
        ("Which is commonly used to pay for goods in India?", "Indian rupees", "Only foreign stamps", "Only school marks", "Only railway tickets", "A"),
        ("What is a need?", "Something necessary for everyday life", "Something that is always a luxury", "A type of shop", "A method of advertising", "A"),
        ("What is a want?", "Something a person would like to have", "Every item essential for survival", "A government tax only", "A type of market road", "A"),
        ("Why do shopkeepers display products?", "To let customers see what is available", "To prevent all customers from entering", "To stop goods from being sold", "To replace money", "A"),
        ("What is bargaining?", "Discussing the price with a seller", "Producing goods in a factory", "Transporting goods by train", "Recording rainfall", "A"),
        ("What does a manufacturer do?", "Produces goods", "Only purchases goods for personal use", "Only delivers court notices", "Only teaches at a school", "A"),
        ("Which is an example of a local service?", "A tailoring service", "A mountain range", "A river basin", "A type of soil", "A"),
        ("What is advertising?", "Communicating information to promote a product or service", "Counting people in a village", "Making a public road", "Conducting an election", "A"),
        ("Why do markets need transport?", "To move goods between producers, sellers, and buyers", "To remove the need for goods", "To stop all communication", "To make prices identical everywhere", "A"),
        ("What is a customer?", "A person who buys goods or services", "A person who only makes laws", "A person who controls the weather", "A person who builds only dams", "A"),
        ("What is a local vendor?", "A person who sells goods in a local area", "A person who only writes textbooks", "A person who conducts court trials", "A person who issues currency", "A"),
        ("Why are markets important?", "They help people exchange goods and services", "They eliminate every human need", "They replace all schools", "They stop production", "A"),
    ],
    "Medium": [
        ("Why can goods be cheaper in a wholesale market?", "Goods are often sold in large quantities, reducing per-unit costs", "Wholesalers never pay for transport", "All goods are provided free", "Retailers are not allowed to buy goods", "A"),
        ("How does a retailer connect producers with consumers?", "By buying goods through supply channels and selling them to customers", "By preventing goods from reaching buyers", "By setting every government policy", "By producing all goods personally", "A"),
        ("Why might the same product have different prices in two markets?", "Transport costs, rent, demand, and competition may differ", "Prices are always fixed by customers' ages", "Products cannot be sold in different places", "All sellers must charge identical prices", "A"),
        ("What is one advantage of a weekly market for customers?", "Several sellers may offer goods in one place, allowing price comparison", "Customers must buy only from one seller", "All products are always free", "It removes every need for transport", "A"),
        ("Why can small traders face difficulties competing with large shops?", "Large shops may benefit from bulk purchasing and greater resources", "Small traders are never allowed to sell goods", "Large shops cannot advertise", "Small traders never have customers", "A"),
        ("How can online markets benefit consumers?", "They can provide access to products from different locations", "They eliminate all delivery costs in every case", "They guarantee that every product is genuine", "They prevent price comparison", "A"),
        ("What is an important risk of buying online?", "The product may differ from its description or be defective", "Every online seller is necessarily dishonest", "Online purchases never require payment", "Online goods cannot be returned under any circumstances", "A"),
        ("How can competition among sellers benefit consumers?", "It may encourage better prices, quality, and service", "It always causes every shop to close", "It prevents consumers from comparing products", "It makes demand irrelevant", "A"),
        ("What does a supply chain describe?", "The stages through which goods move from producers to consumers", "The process of writing a school timetable", "The structure of a court", "The movement of planets only", "A"),
        ("Why do producers often depend on traders?", "Traders help distribute products to different markets", "Traders make production unnecessary", "Traders prevent customers from buying goods", "Traders replace all transport systems", "A"),
        ("How can advertising influence consumer choices?", "It can inform buyers and encourage interest in particular products", "It guarantees that a product is always the best", "It removes the need to consider price", "It makes every claim scientifically proven", "A"),
        ("Why should consumers check product labels?", "Labels can provide information about price, quantity, ingredients, and expiry dates", "Labels always guarantee perfect quality", "Labels remove the need to inspect products", "Labels show only the shopkeeper's name", "A"),
        ("What is one function of money in a market?", "It provides a commonly accepted medium of exchange", "It eliminates the need for production", "It guarantees equal incomes", "It replaces all goods and services", "A"),
        ("Why is barter sometimes difficult?", "Both parties must want what the other offers", "Barter always requires a bank card", "Barter makes exchanging goods impossible", "Barter requires every product to have the same weight", "A"),
        ("What can happen when demand increases but supply stays limited?", "Prices may rise", "Prices must always fall to zero", "All products become free", "Demand disappears automatically", "A"),
        ("Why do some consumers prefer local markets?", "They may offer convenient access and familiar sellers", "Local markets always sell every product at the lowest price", "Local markets never require money", "Local markets cannot provide fresh goods", "A"),
        ("What is the role of transport in market distribution?", "It connects production locations with selling and consumption locations", "It makes storage and delivery unnecessary", "It determines the quality of every product", "It prevents goods from crossing regions", "A"),
        ("Why may farmers receive only a small share of the final retail price?", "Intermediaries, transport, storage, and other costs may take part of the price", "Farmers always set the final shop price", "Retailers never have operating costs", "Consumers pay no money for farm products", "A"),
        ("How can a consumer make a more informed purchase?", "Compare price, quality, quantity, and product information", "Choose only the most colourful package", "Ignore expiry dates", "Buy every advertised product", "A"),
        ("What is market demand?", "The quantity consumers are willing and able to buy at different prices", "The number of shops in a city only", "The total amount of rainfall", "The number of products stored in one warehouse only", "A"),
        ("What is market supply?", "The quantity sellers are willing and able to offer for sale at different prices", "The number of people attending a school", "The total number of advertisements only", "The amount of money kept in a household", "A"),
        ("How can cold storage help agricultural markets?", "It can slow spoilage and extend the period products remain usable", "It makes all crops grow without water", "It removes every transport cost", "It guarantees that prices never change", "A"),
        ("Why can a middleman play a useful role?", "They may connect producers to buyers and organise distribution", "They always eliminate every cost", "They make consumers unnecessary", "They prevent all goods from reaching markets", "A"),
        ("What is one possible disadvantage of excessive packaging?", "It can increase costs and create additional waste", "It always improves the nutritional value of food", "It removes transport requirements", "It guarantees that a product never expires", "A"),
        ("How does digital payment affect market transactions?", "It allows payments to be made electronically", "It eliminates the need to check transaction records", "It guarantees every online seller is genuine", "It makes all products free", "A"),
        ("Why is consumer protection important?", "It helps address unfair practices and unsafe or misleading products", "It guarantees every buyer will like every product", "It prevents consumers from asking questions", "It removes all market competition", "A"),
        ("What is a wholesale-retail relationship?", "Retailers often purchase goods from wholesalers for resale to consumers", "Wholesalers buy every item only for personal use", "Retailers always manufacture all products", "Consumers are not involved in retail markets", "A"),
        ("How can a market create employment?", "It provides work in selling, transport, storage, and related services", "It prevents people from earning income", "It removes all demand for skills", "It eliminates the need for producers", "A"),
        ("Why may a seller offer discounts?", "To attract buyers, clear stock, or respond to competition", "To make all goods permanently unavailable", "To prevent transactions", "To eliminate product demand", "A"),
        ("What does fair trade generally aim to support?", "Fairer trading relationships and treatment of producers and workers", "The exclusion of all small producers", "The removal of product quality standards", "The prevention of consumer choice", "A"),
    ],
    "Hard": [
        ("A farmer sells vegetables to a trader, who sells them to a wholesaler, then a retailer, and finally a consumer. What does this illustrate?", "A chain of intermediaries in market distribution", "Direct barter between the farmer and every consumer", "The absence of a supply chain", "A government election process", "A"),
        ("A product's demand rises sharply while its supply remains unchanged. What is a likely market outcome, all else equal?", "Its price may increase", "Its price must become zero", "Its supply instantly becomes unlimited", "Consumers no longer want the product", "A"),
        ("A large retailer buys goods in bulk and negotiates lower prices from suppliers. What advantage does this show?", "Economies of scale and stronger purchasing power", "The complete absence of operating costs", "The elimination of all consumer demand", "A guarantee of perfect product quality", "A"),
        ("A farmer's product spoils before reaching distant markets. Which investment could directly reduce this problem?", "Improved storage and cold-chain facilities", "More decorative packaging only", "Fewer transport connections", "Removing product information labels", "A"),
        ("An online seller displays a low price but adds large undisclosed fees at checkout. What is the main concern?", "Lack of transparent pricing and potentially misleading selling practices", "Competition has eliminated every consumer risk", "The buyer is guaranteed a refund", "The product must be counterfeit", "A"),
        ("A village has only one seller of an essential product, with no close alternatives. Which market condition is most likely?", "Limited competition may reduce consumers' choices", "Perfect competition is guaranteed", "Prices must always be lowest", "Consumers can choose among unlimited sellers", "A"),
        ("Why might the retail price of a product be much higher than the amount received by its producer?", "Distribution costs, intermediaries, storage, and retail expenses contribute to the final price", "The producer always receives the entire retail price", "Retailing has no costs", "The final price never includes transport", "A"),
        ("A company advertises a product as having benefits unsupported by evidence. What should a responsible consumer do?", "Seek reliable information and avoid relying solely on the claim", "Assume the advertisement has been independently verified", "Ignore all product labels and evidence", "Buy it because advertising claims are legally guaranteed to be true", "A"),
        ("Two shops sell comparable goods. One improves service and reduces prices after a competitor opens nearby. What is this an example of?", "Competition influencing sellers' behaviour", "Barter replacing money", "The elimination of consumer choice", "The absence of market demand", "A"),
        ("A market has high demand but poor roads make delivery expensive. Which factor most directly contributes to higher final prices?", "Transport and distribution costs", "The spelling of the product name", "The colour of the seller's clothing", "The number of school subjects nearby", "A"),
        ("A producer sells directly to consumers through an online platform. What may be reduced?", "Dependence on some traditional intermediaries", "The need to produce goods", "The need for product quality", "Every possible delivery cost", "A"),
        ("Why does buying in bulk not always benefit every consumer?", "It may require more upfront money and can lead to waste if goods are unused", "Bulk purchases always cost more per unit", "Bulk goods cannot be stored", "Bulk purchases never change the quantity purchased", "A"),
        ("A consumer chooses a product solely because it has the most attractive packaging. What important decision factors may have been neglected?", "Price, quality, quantity, safety, and suitability", "The colour of the shop building only", "The seller's preferred music", "The number of streets in the area", "A"),
        ("A market depends on one distant supplier, and transport is disrupted. What is a likely consequence?", "Shortages or delays may occur", "Supply is guaranteed to increase", "Prices must immediately fall", "Consumers no longer need the product", "A"),
        ("How can digital marketplaces create opportunities for small producers?", "They may help producers reach customers beyond their immediate locality", "They guarantee free delivery in all circumstances", "They eliminate competition", "They ensure every product sells immediately", "A"),
        ("A seller uses a faulty weighing scale to charge customers for less quantity than stated. Which issue is illustrated?", "An unfair trade practice that harms consumers", "A normal form of transparent pricing", "A benefit of perfect competition", "A method of improving product safety", "A"),
        ("Why might a consumer prefer a product with a higher initial price but longer durability?", "Its total cost over the period of use may be lower", "Higher prices always guarantee quality", "Durability is unrelated to value", "The product will never require maintenance", "A"),
        ("What can happen when many intermediaries operate in a supply chain without adding sufficient value?", "Costs may rise and the producer's share may be reduced", "The final price must become zero", "All distribution activities become unnecessary", "Consumers automatically receive more quantity", "A"),
        ("A seller lowers prices to clear seasonal stock before it spoils. What is the likely business reason?", "Reducing inventory losses and recovering some costs", "Making the product impossible to purchase", "Increasing spoilage intentionally", "Eliminating all future demand", "A"),
        ("Why is reliable product information especially important for food and medicines?", "It can help consumers assess safety, ingredients, dosage or use, and expiry information", "It guarantees that no product can ever cause harm", "It makes professional advice unnecessary", "It removes the need for quality controls", "A"),
        ("A government improves rural roads linking farms to towns. How could this affect markets?", "It may reduce delivery delays and improve access to buyers", "It necessarily eliminates every intermediary", "It guarantees identical prices everywhere", "It stops agricultural production", "A"),
        ("Why can a low advertised price be an incomplete measure of value?", "Quality, durability, hidden fees, and maintenance costs may also matter", "Price is never relevant to consumers", "The lowest price always means the best quality", "All products have identical lifetime costs", "A"),
        ("A seller receives many online orders but regularly fails to deliver them. Which factor is most important when assessing the seller?", "Reliability and fulfilment performance, alongside price", "The number of colours on the website", "The length of the product title only", "The seller's use of decorative fonts", "A"),
        ("What is a possible economic effect when cold storage reduces food spoilage?", "More produce may reach markets and be sold over a longer period", "All agricultural prices become fixed", "Farmers no longer need to grow crops", "Transport becomes unnecessary", "A"),
        ("A small producer cooperates with other producers to market products collectively. What potential benefit can result?", "Shared costs and stronger bargaining power", "A guarantee that every product sells at any price", "The elimination of all quality requirements", "The end of consumer choice", "A"),
        ("Why might a market price differ between peak and off-season periods for fruit?", "Seasonal changes in availability can affect supply and prices", "Fruit prices depend only on the colour of the shop", "Seasonality never affects supply", "All sellers must use the same price at all times", "A"),
        ("A product becomes popular after a campaign, but production cannot expand quickly. What is a likely short-term effect?", "Demand may exceed supply and put upward pressure on price", "Supply instantly becomes unlimited", "The product becomes free", "The demand disappears by definition", "A"),
        ("How can consumer reviews be useful but imperfect?", "They provide experiences but may be biased, fake, or unrepresentative", "Every review is independently verified", "Negative reviews are always false", "Reviews replace product testing in every case", "A"),
        ("A retailer gives a discount but reduces the package quantity. What should consumers compare?", "Unit price and quantity as well as the displayed discount", "Only the size of the discount label", "Only the package colour", "Only the number of advertisements", "A"),
        ("Which combination best describes a well-functioning market?", "Informed consumers, fair practices, accessible distribution, and meaningful competition", "Hidden fees, misleading claims, and no consumer choices", "Unverified advertising and deliberately faulty measures", "Restricted information and no product standards", "A"),
    ],
}


def main():
    db = SessionLocal()
    added = 0

    try:
        lesson = (
            db.query(Lesson)
            .filter(
                Lesson.title == "Markets Around Us",
                Lesson.topic == "Social Science",
            )
            .first()
        )

        if not lesson:
            print("ERROR: Markets Around Us lesson was not found.")
            print("Check the lesson title and topic in the database.")
            return

        for difficulty, questions in QUESTION_BANK.items():
            quiz = (
                db.query(Quiz)
                .filter(
                    Quiz.lesson_id == lesson.id,
                    Quiz.difficulty == difficulty,
                )
                .first()
            )

            if not quiz:
                quiz = Quiz(
                    lesson_id=lesson.id,
                    title=f"{lesson.title} - {difficulty}",
                    difficulty=difficulty,
                )
                db.add(quiz)
                db.flush()

            existing = (
                db.query(Question)
                .filter(Question.quiz_id == quiz.id)
                .all()
            )

            if len(existing) >= 30:
                print(f"{difficulty}: already has {len(existing)} questions; skipped.")
                continue

            existing_texts = {q.question.strip().lower() for q in existing}

            for item in questions:
                if len(existing) >= 30:
                    break

                question_text, a, b, c, d, correct_letter = item

                if question_text.strip().lower() in existing_texts:
                    continue

                options = [a, b, c, d]
                correct_text = options[ord(correct_letter) - ord("A")]
                random.shuffle(options)
                new_correct_letter = "ABCD"[options.index(correct_text)]

                db.add(
                    Question(
                        quiz_id=quiz.id,
                        question=question_text,
                        option_a=options[0],
                        option_b=options[1],
                        option_c=options[2],
                        option_d=options[3],
                        correct_answer=new_correct_letter,
                    )
                )

                existing_texts.add(question_text.strip().lower())
                existing.append(None)
                added += 1

        db.commit()

        print("\nFINAL VERIFICATION")
        total = 0

        for difficulty in QUESTION_BANK:
            quiz = (
                db.query(Quiz)
                .filter(
                    Quiz.lesson_id == lesson.id,
                    Quiz.difficulty == difficulty,
                )
                .first()
            )

            count = (
                db.query(Question)
                .filter(Question.quiz_id == quiz.id)
                .count()
                if quiz
                else 0
            )

            total += count
            print(f"{difficulty}: {count}/30")

        print(f"TOTAL: {total}/90")
        print(f"New questions added: {added}")

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()