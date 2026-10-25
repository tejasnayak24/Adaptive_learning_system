import sqlite3
from pathlib import Path

DATABASE_PATH = (
    Path(__file__).resolve().parent.parent
    / "adaptive_learning.db"
)

TARGET_QUESTIONS = 30

# Format:
# Question, Option A, Option B, Option C, Option D, Correct Answer

QUESTION_BANK = {
    "Easy": [
        ("What is the basic structural unit of life?", "Cell", "Tissue", "Organ", "Organ system", "A"),
        ("Which cell structure contains genetic material?", "Cell membrane", "Nucleus", "Cytoplasm", "Vacuole", "B"),
        ("Which organelle is commonly called the powerhouse of the cell?", "Golgi apparatus", "Lysosome", "Chloroplast", "Mitochondrion", "D"),
        ("What jelly-like material fills much of a cell?", "Cytoplasm", "Cell wall", "Chromosome", "Nucleolus", "A"),
        ("Which structure gives plant cells additional support?", "Cell membrane", "Cell wall", "Ribosome", "Mitochondrion", "B"),
        ("Which organelle carries out photosynthesis?", "Nucleus", "Lysosome", "Chloroplast", "Golgi apparatus", "C"),
        ("Which structures make proteins?", "Vacuoles", "Lysosomes", "Chloroplasts", "Ribosomes", "D"),
        ("Which type of cell lacks a membrane-bound nucleus?", "Prokaryotic cell", "Plant cell", "Animal cell", "Fungal cell", "A"),
        ("Which instrument is commonly used to observe cells?", "Telescope", "Microscope", "Periscope", "Barometer", "B"),
        ("Which organelle contains digestive enzymes?", "Ribosome", "Nucleolus", "Chloroplast", "Lysosome", "D"),
        ("What is a group of similar cells performing a common function called?", "Tissue", "Organ", "Organism", "Organelle", "A"),
        ("Which cell component stores water and other substances?", "Ribosome", "Vacuole", "Centromere", "Nucleolus", "B"),
        ("Which molecule carries hereditary information in most organisms?", "Starch", "Cellulose", "DNA", "Glucose", "C"),
        ("What is the smallest living unit capable of carrying out life processes?", "Organ", "Tissue", "Organ system", "Cell", "D"),
        ("Which organelle modifies and packages many proteins?", "Lysosome", "Golgi apparatus", "Centrosome", "Chloroplast", "B"),
        ("Which structure separates the nucleus from the cytoplasm?", "Cell wall", "Vacuole", "Ribosome", "Nuclear envelope", "D"),
        ("Which structure is generally present in plant cells but absent in animal cells?", "Chloroplast", "Cell membrane", "Cytoplasm", "Mitochondrion", "A"),
        ("Which cell structure helps maintain cell shape?", "Nucleolus", "Cytoskeleton", "Chromosome only", "Nuclear pore", "B"),
        ("What is the process by which one cell divides into daughter cells called?", "Digestion", "Respiration", "Cell division", "Photosynthesis", "C"),
        ("Which organelle is involved in lipid synthesis?", "Ribosome", "Nucleolus", "Chloroplast", "Smooth endoplasmic reticulum", "D"),
        ("Which type of cell usually has a large central vacuole?", "Red blood cell", "Bacterial cell", "Animal muscle cell", "Mature plant cell", "D"),
        ("Which structure contains chromosomes in a typical plant cell?", "Nucleus", "Vacuole", "Cell wall", "Golgi apparatus", "A"),
        ("Which structure surrounds the cytoplasm in an animal cell?", "Cell wall", "Chloroplast", "Cell membrane", "Capsule only", "C"),
        ("Which organelle contains chlorophyll?", "Mitochondrion", "Lysosome", "Golgi apparatus", "Chloroplast", "D"),
        ("Which structure is responsible for producing ribosome subunits?", "Nucleolus", "Vacuole", "Cell wall", "Lysosome", "A"),
        ("Which part of a cell contains many enzymes for chemical reactions?", "Cell wall", "Cytoplasm", "Chromosome", "Nuclear envelope", "B"),
        ("Which structure protects the contents of a plant cell and helps maintain its shape?", "Ribosome", "Nucleolus", "Cell wall", "Golgi apparatus", "C"),
        ("Which organelle produces much of the ATP in aerobic eukaryotic cells?", "Vacuole", "Lysosome", "Golgi apparatus", "Mitochondrion", "D"),
        ("What is the main function of ribosomes?", "Protein synthesis", "Water storage", "Photosynthesis", "Waste removal only", "A"),
        ("Which structure regulates what enters and leaves a cell?", "Nucleolus", "Cell membrane", "Chromosome", "Ribosome", "B"),
    ],

    "Medium": [
        ("Why do most cells remain relatively small?", "They cannot contain DNA", "A high surface-area-to-volume ratio supports exchange", "Small cells have no cytoplasm", "Large cells cannot use energy", "B"),
        ("What is the main function of rough endoplasmic reticulum?", "Store hereditary information", "Produce cellular energy directly", "Help synthesize and process proteins", "Carry out photosynthesis", "C"),
        ("Which process moves water across a selectively permeable membrane?", "Active transport", "Endocytosis", "Exocytosis", "Osmosis", "D"),
        ("What is the main role of the nucleolus?", "Ribosome subunit production", "ATP storage", "Lipid digestion", "Photosynthesis", "A"),
        ("Which organelle is most directly involved in aerobic cellular respiration?", "Golgi apparatus", "Mitochondrion", "Vacuole", "Lysosome", "B"),
        ("What may happen to an animal cell in a strongly hypotonic solution?", "It loses all water", "It develops a cell wall", "It may swell and burst", "It stops containing DNA", "C"),
        ("Which feature distinguishes eukaryotic cells from prokaryotic cells?", "They always have a cell wall", "They lack ribosomes", "They have no genetic material", "They contain a membrane-bound nucleus", "D"),
        ("What is the role of the plant cell wall?", "Provide support and resist excessive swelling", "Control all gene expression", "Produce proteins", "Generate all cellular ATP", "A"),
        ("Which process allows a cell to engulf a large particle?", "Diffusion", "Phagocytosis", "Osmosis", "Simple filtration", "B"),
        ("Why are mitochondria abundant in many muscle cells?", "They perform photosynthesis", "They lack nuclei", "Muscle contraction requires substantial energy", "They store chromosomes only", "C"),
        ("Which organelle sorts many proteins for delivery?", "Lysosome", "Ribosome", "Nucleolus", "Golgi apparatus", "D"),
        ("What is the main function of a selectively permeable membrane?", "Regulate movement of substances", "Allow every substance to enter freely", "Store all cellular DNA", "Replace the cytoplasm", "A"),
        ("Which process produces two genetically similar daughter cells for growth and repair?", "Meiosis", "Mitosis", "Fertilization", "Transcription", "B"),
        ("What is the function of lysosomes?", "Capture sunlight", "Copy chromosomes", "Break down materials using enzymes", "Synthesize DNA from sunlight", "C"),
        ("Which structure is part of the endomembrane system?", "Chromosome", "Centriole only", "Nucleoid", "Endoplasmic reticulum", "D"),
        ("What does diffusion describe?", "Net movement from higher to lower concentration", "Movement requiring ATP in every case", "Movement of water only", "Movement against a concentration gradient", "A"),
        ("Why do mature mammalian red blood cells lack nuclei?", "They perform photosynthesis", "This leaves more space for haemoglobin", "They divide rapidly in circulation", "They contain a cell wall instead", "B"),
        ("Which structure helps organize microtubules during many animal-cell divisions?", "Lysosome", "Vacuole", "Centrosome", "Golgi apparatus", "C"),
        ("What is the principal role of messenger RNA?", "Store energy as ATP", "Build the cell wall directly", "Digest old organelles", "Carry genetic instructions for protein synthesis", "D"),
        ("Which process releases materials from a cell using vesicles?", "Exocytosis", "Osmosis", "Diffusion", "Phagocytosis", "A"),
        ("What is the main function of smooth endoplasmic reticulum?", "Translate messenger RNA", "Lipid synthesis and certain detoxification reactions", "Store chromosomes", "Produce ribosomal subunits", "B"),
        ("Which statement about chloroplasts is correct?", "They occur in all animal cells", "They perform glycolysis only", "They contain chlorophyll for photosynthesis", "They replace the nucleus", "C"),
        ("What is cellular differentiation?", "Destruction of all cellular DNA", "Movement of water through membranes", "Production of ATP without nutrients", "Development of specialized cell structures and functions", "D"),
        ("What is the main role of transfer RNA during translation?", "Bring amino acids to the ribosome", "Copy the entire genome", "Digest proteins in lysosomes", "Build phospholipids", "A"),
        ("Why are ribosomes essential to cells?", "They store cellular water", "They assemble proteins from amino acids", "They carry out every reaction", "They form the nuclear envelope only", "B"),
        ("What is the main function of the nuclear envelope?", "Produce ATP", "Digest proteins", "Separate the nucleus from the cytoplasm", "Carry out photosynthesis", "C"),
        ("Which process allows oxygen to move from an area of higher concentration to lower concentration?", "Active transport", "Endocytosis", "Exocytosis", "Diffusion", "D"),
        ("Which organelle is responsible for modifying many proteins after synthesis?", "Golgi apparatus", "Nucleolus", "Cell wall", "Centrosome", "A"),
        ("What is the main role of the plasma membrane?", "Store chromosomes", "Control exchange between cell and environment", "Produce all cellular proteins", "Perform photosynthesis in animals", "B"),
        ("Which structure contains enzymes that help break down worn-out cell components?", "Ribosome", "Nucleolus", "Lysosome", "Cell wall", "C"),
    ],

    "Hard": [
        ("A cell is placed in a hypertonic solution. What is the most likely immediate effect?", "Water enters and the cell swells", "Solute instantly disappears", "Water leaves the cell by osmosis", "The nucleus divides immediately", "C"),
        ("A substance crosses a membrane down its concentration gradient with help from a carrier protein but without ATP. What is this?", "Primary active transport", "Endocytosis", "Simple diffusion through the lipid bilayer", "Facilitated diffusion", "D"),
        ("A drug blocks mitochondrial ATP production. Which process is most directly affected?", "ATP-dependent active transport", "Passive diffusion of oxygen", "Osmosis", "Simple diffusion of carbon dioxide", "A"),
        ("A mutation prevents a protein from entering the rough ER. Which pathway might be affected?", "DNA replication", "The secretory pathway", "The genetic code itself", "Photosynthesis in animal cells", "B"),
        ("Which observation supports the endosymbiotic origin of mitochondria?", "They contain digestive enzymes", "They are surrounded by cytoplasm", "They possess their own DNA and bacterial-like ribosomes", "They occur in every prokaryote", "C"),
        ("Which structure limits excessive expansion of a turgid plant cell?", "Ribosome", "Nucleolus", "Golgi apparatus", "Rigid cell wall", "D"),
        ("A cell has abundant rough ER and Golgi apparatus. Which function is it likely specialized for?", "Secretion of proteins", "Storage of genetic code outside DNA", "Photosynthesis in darkness", "Movement using flagella only", "A"),
        ("A competitive inhibitor binds an enzyme's active site. What is the direct consequence?", "All enzyme molecules are destroyed", "Substrate binding is reduced at that site", "ATP becomes a chromosome", "The membrane becomes impermeable to water", "B"),
        ("During mitosis, chromosomes fail to separate correctly. What may result?", "All daughter cells become bacteria", "Photosynthesis stops in every organism", "Daughter cells receive abnormal chromosome numbers", "The membrane becomes a cell wall", "C"),
        ("A cell's lysosomal membrane ruptures extensively. What may happen?", "The cell begins photosynthesis", "Chromosomes become lipids", "Ribosomes stop forming in every tissue", "Digestive enzymes may damage cellular components", "D"),
        ("Which change would increase simple diffusion rate, all else equal?", "Increasing the concentration gradient", "Increasing membrane thickness", "Reducing membrane surface area", "Removing the diffusing substance", "A"),
        ("A poison inhibits the sodium-potassium pump. What is expected over time?", "DNA converts into glucose", "Ion gradients across the membrane deteriorate", "All passive diffusion instantly stops", "The cell develops chloroplasts", "B"),
        ("A mutation disrupts the spindle apparatus during mitosis. Which event is impaired?", "Translation at ribosomes", "Lipid synthesis", "Accurate chromosome segregation", "Diffusion of oxygen", "C"),
        ("Why can a single-celled organism function without tissues or organs?", "It has no need for energy", "It lacks a plasma membrane", "It contains no genetic information", "One cell performs essential life processes", "D"),
        ("A membrane allows water through but not a dissolved solute. What explains water movement?", "Osmotic gradients", "Chromosome crossing-over", "Protein translation", "Independent assortment alone", "A"),
        ("Which result best indicates apoptosis?", "Uncontrolled growth without regulation", "Regulated cell dismantling with characteristic changes", "Formation of a bacterial cell wall", "Conversion of proteins into DNA", "B"),
        ("A mutation disrupts the mitochondrial inner membrane. Which process is most directly compromised?", "Nuclear DNA replication only", "Lysosomal digestion only", "Oxidative phosphorylation", "Passive diffusion across the cell membrane only", "C"),
        ("Which route is typical for a protein destined for the plasma membrane?", "Nucleus directly to surface", "Lysosome to nucleolus", "Chloroplast to mitochondrion", "Rough ER, Golgi apparatus, then transport vesicles", "D"),
        ("Why does increasing cell size without proportional surface-area growth create transport challenges?", "Volume increases faster than surface area", "DNA disappears as cells grow", "Membranes stop containing lipids", "Large cells cannot contain water", "A"),
        ("A cell has ribosomes but no membrane-bound organelles. What is a reasonable conclusion?", "It must be an animal cell", "It may be a prokaryotic cell", "It must contain chloroplasts", "It cannot synthesize proteins", "B"),
        ("A cell's DNA is intact, but ribosomes are inhibited. Which process is directly reduced?", "Water diffusion", "Oxygen movement", "Protein synthesis", "Membrane lipid diffusion", "C"),
        ("A chemical prevents vesicles from fusing with the plasma membrane. Which process is impaired?", "Osmosis", "Simple diffusion", "Chromosome replication", "Exocytosis", "D"),
        ("Why can phospholipids form a bilayer in water?", "Hydrophilic heads and hydrophobic tails interact differently with water", "Both ends repel water equally", "They are made entirely of DNA", "They require a cell wall", "A"),
        ("A glucose transporter that moves glucose down its concentration gradient is defective. Which mechanism is impaired?", "Simple diffusion of water", "Facilitated diffusion", "DNA replication", "Phagocytosis", "B"),
        ("Which observation distinguishes active transport from facilitated diffusion?", "Both always move substances against gradients", "Neither uses membrane proteins", "Active transport can move substances against gradients using energy", "Facilitated diffusion always consumes ATP directly", "C"),
        ("A mutation damages the mitochondrial electron transport chain. What is likely to decrease?", "Passive water movement", "DNA's chemical identity", "Ribosome number in every cell", "ATP production by oxidative phosphorylation", "D"),
        ("A cell is placed in an isotonic solution. What is expected?", "No net water movement across the membrane", "Water only enters the cell", "Water only leaves the cell", "The membrane disappears", "A"),
        ("Which event occurs during cytokinesis?", "DNA is translated into protein", "The cytoplasm divides between daughter cells", "ATP becomes DNA", "The nucleus performs photosynthesis", "B"),
        ("Why does a membrane transport protein show selectivity?", "All molecules have identical shapes", "Membranes contain no lipids", "Its structure and chemical properties favor particular substances", "Every substance must use ATP", "C"),
        ("A cell cannot produce sufficient ATP. Which energy-dependent activity is likely to be affected?", "Simple diffusion", "Osmosis", "Passive movement of oxygen", "Active transport against a concentration gradient", "D"),
    ],
}


def normalize(text):
    """Normalize question text for duplicate detection."""
    return " ".join(text.casefold().split())


def main():
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(
            f"Database not found: {DATABASE_PATH}"
        )

    connection = sqlite3.connect(DATABASE_PATH)

    try:
        connection.execute("PRAGMA foreign_keys = ON")

        # Confirm the exact lesson.
        lesson = connection.execute(
            """
            SELECT id
            FROM lessons
            WHERE lower(trim(title)) = lower(trim(?))
              AND lower(trim(topic)) = lower(trim(?))
            """,
            ("Cell Biology", "Cell Biology"),
        ).fetchone()

        if lesson is None:
            raise RuntimeError(
                "Cell Biology lesson was not found. "
                "No questions were inserted."
            )

        lesson_id = lesson[0]
        total_inserted = 0

        # All three difficulty levels run in one transaction.
        with connection:
            for difficulty, candidates in QUESTION_BANK.items():

                quiz = connection.execute(
                    """
                    SELECT id
                    FROM quizzes
                    WHERE lesson_id = ?
                      AND lower(trim(difficulty)) = lower(trim(?))
                    """,
                    (lesson_id, difficulty),
                ).fetchone()

                if quiz is None:
                    raise RuntimeError(
                        f"Missing {difficulty} quiz. "
                        "No changes were committed."
                    )

                quiz_id = quiz[0]

                existing_rows = connection.execute(
                    """
                    SELECT question
                    FROM questions
                    WHERE quiz_id = ?
                    """,
                    (quiz_id,),
                ).fetchall()

                existing_questions = {
                    normalize(row[0]) for row in existing_rows
                }

                current_count = len(existing_rows)

                if current_count > TARGET_QUESTIONS:
                    raise RuntimeError(
                        f"{difficulty} already has {current_count} "
                        f"questions; target is {TARGET_QUESTIONS}."
                    )

                inserted_for_level = 0

                for item in candidates:
                    if current_count >= TARGET_QUESTIONS:
                        break

                    text, a, b, c, d, answer = item
                    normalized_text = normalize(text)

                    # Validate the candidate.
                    if not text.strip():
                        raise ValueError("An empty question was found.")

                    if answer not in {"A", "B", "C", "D"}:
                        raise ValueError(
                            f"Invalid correct answer for: {text}"
                        )

                    if not all(
                        option.strip() for option in (a, b, c, d)
                    ):
                        raise ValueError(
                            f"An empty option was found for: {text}"
                        )

                    # Skip questions already in the database or bank.
                    if normalized_text in existing_questions:
                        print(
                            f"Skipping duplicate ({difficulty}): {text}"
                        )
                        continue

                    connection.execute(
                        """
                        INSERT INTO questions (
                            quiz_id,
                            question,
                            option_a,
                            option_b,
                            option_c,
                            option_d,
                            correct_answer
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        """,
                        (quiz_id, text, a, b, c, d, answer),
                    )

                    existing_questions.add(normalized_text)
                    current_count += 1
                    inserted_for_level += 1
                    total_inserted += 1

                if current_count != TARGET_QUESTIONS:
                    raise RuntimeError(
                        f"{difficulty} has only {current_count} questions "
                        f"after processing the bank; target is "
                        f"{TARGET_QUESTIONS}. Add more unique questions "
                        "to this difficulty's QUESTION_BANK. "
                        "The transaction will be rolled back."
                    )

                print(
                    f"{difficulty}: added {inserted_for_level}; "
                    f"final count = {current_count}"
                )

        print("\nCell Biology question expansion completed!")
        print(f"New questions inserted: {total_inserted}")
        print("Easy: 30 questions")
        print("Medium: 30 questions")
        print("Hard: 30 questions")
        print("Other lessons and Social Science were not modified.")

    finally:
        connection.close()


if __name__ == "__main__":
    main()