"""
Seed the Adaptive Learning System with an initial Science curriculum.

Creates:
- 5 Science lessons
- 15 quizzes (Easy/Medium/Hard for each lesson)
- 75 questions (5 per difficulty per lesson)

Run from the project root:
    python backend/seed_science.py
"""

from pathlib import Path
import sys

BACKEND_DIR = Path(__file__).resolve().parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.database.connection import SessionLocal
from app.models.student import Student
from app.models.lesson import Lesson
from app.models.quiz import Quiz
from app.models.question import Question
from app.models.progress import Progress
from app.models.session import LearningSession
from app.models.reward import RewardHistory

LESSONS = [{'title': 'Cell Biology', 'topic': 'Cell Biology', 'content': 'Cells are the basic structural and functional units of living organisms. Most cells contain a cell membrane, cytoplasm, genetic material and ribosomes. Eukaryotic cells also contain membrane-bound organelles. The nucleus stores most of the genetic material and helps control cell activities. Mitochondria release usable energy through cellular respiration. Ribosomes make proteins. Plant cells additionally contain a cell wall, chloroplasts for photosynthesis and a large central vacuole. Cells maintain stable internal conditions through processes such as diffusion, osmosis and active transport.', 'quizzes': [('Easy', [('What is the basic structural and functional unit of life?', 'Organ', 'Cell', 'Tissue', 'Organ system', 'B'), ("Which organelle contains most of a eukaryotic cell's DNA?", 'Nucleus', 'Ribosome', 'Vacuole', 'Cell wall', 'A'), ('Which organelle is mainly responsible for producing ATP during cellular respiration?', 'Chloroplast', 'Ribosome', 'Mitochondrion', 'Nucleus', 'C'), ('Which structure controls what enters and leaves a cell?', 'Cell membrane', 'Nucleus', 'Cytoplasm', 'Ribosome', 'A'), ('Which structure is found in plant cells but not animal cells?', 'Cell membrane', 'Cytoplasm', 'Cell wall', 'Ribosome', 'C')]), ('Medium', [('What is the main function of ribosomes?', 'Store DNA', 'Make proteins', 'Produce sunlight', 'Digest chromosomes', 'B'), ('What process is the movement of water across a selectively permeable membrane?', 'Diffusion', 'Osmosis', 'Respiration', 'Photosynthesis', 'B'), ('Why do plant cells contain chloroplasts?', 'To store DNA', 'To make proteins', 'To carry out photosynthesis', 'To digest waste', 'C'), ('What would most directly happen if a cell membrane lost its selective permeability?', 'The cell could not regulate substances entering and leaving', 'The nucleus would disappear', 'DNA would become protein', 'The cell would stop having cytoplasm', 'A'), ('Which structure provides support and protection outside the plant cell membrane?', 'Nucleus', 'Cell wall', 'Ribosome', 'Mitochondrion', 'B')]), ('Hard', [('A cell is placed in a solution with a much higher solute concentration than its cytoplasm. What is most likely to happen?', 'Water enters the cell', 'Water leaves the cell', 'No water movement occurs', 'The cell immediately divides', 'B'), ('Why can a cell with many mitochondria generally support high energy demand?', 'Mitochondria store chromosomes', 'They increase protein storage', 'They provide greater capacity for ATP production', 'They prevent diffusion', 'C'), ('A mutation prevents ribosomes from functioning. Which process would be directly affected first?', 'Protein synthesis', 'DNA storage', 'Water movement', 'Cell wall formation only', 'A'), ('Why is a very large cell less efficient at exchanging materials with its environment?', 'It has more DNA', 'Its surface-area-to-volume ratio decreases', 'It cannot contain cytoplasm', 'Its nucleus becomes smaller', 'B'), ('A plant is kept in darkness for a long period. Which cellular process is directly reduced because chloroplasts cannot receive light energy?', 'Photosynthesis', 'Diffusion', 'Osmosis', 'Protein digestion', 'A')])]}, {'title': 'Human Body Systems', 'topic': 'Human Body Systems', 'content': 'The human body is organized into interacting organ systems. The digestive system breaks food into nutrients that can be absorbed. The respiratory system exchanges oxygen and carbon dioxide. The circulatory system transports gases, nutrients, hormones and wastes through blood. The nervous system detects information and coordinates rapid responses, while the endocrine system uses hormones for longer-lasting regulation. The kidneys help remove wastes and regulate water and ion balance. The muscular and skeletal systems work together to produce movement and provide support. Homeostasis is the maintenance of relatively stable internal conditions despite changes in the environment.', 'quizzes': [('Easy', [('Which system is mainly responsible for exchanging oxygen and carbon dioxide?', 'Digestive', 'Respiratory', 'Skeletal', 'Endocrine', 'B'), ('Which organ pumps blood around the body?', 'Lung', 'Kidney', 'Heart', 'Stomach', 'C'), ('Which system breaks food into smaller molecules for absorption?', 'Digestive', 'Nervous', 'Skeletal', 'Respiratory', 'A'), ('Which organs filter wastes from the blood and help regulate water balance?', 'Lungs', 'Kidneys', 'Bones', 'Pancreas', 'B'), ('Which system coordinates rapid responses to stimuli?', 'Nervous', 'Digestive', 'Skeletal', 'Circulatory', 'A')]), ('Medium', [('What is the main role of red blood cells?', 'Fight all infections', 'Carry oxygen', 'Digest proteins', 'Produce hormones', 'B'), ('Why does the small intestine have many folds and villi?', 'To increase surface area for nutrient absorption', 'To pump blood', 'To store urine', 'To produce oxygen', 'A'), ('Which two systems work together most directly to deliver oxygen from the lungs to body cells?', 'Digestive and skeletal', 'Respiratory and circulatory', 'Nervous and skeletal', 'Endocrine and digestive', 'B'), ('What is homeostasis?', 'Rapid body growth', 'Maintenance of stable internal conditions', 'Breakdown of all food', 'Production of only red blood cells', 'B'), ('What is one major difference between nervous and endocrine regulation?', 'Nervous signals are generally rapid while hormones often act more slowly', 'Hormones never travel through blood', 'The nervous system only controls digestion', 'The endocrine system has no chemical signals', 'A')]), ('Hard', [('During exercise, breathing and heart rate increase together. What is the main advantage of this response?', 'To reduce oxygen delivery', 'To increase oxygen delivery and carbon dioxide removal', 'To stop muscle activity', 'To prevent blood circulation', 'B'), ('If the kidneys fail to regulate water and ions effectively, which homeostatic function is most directly affected?', 'Fluid and electrolyte balance', 'Vision', 'Hearing', 'Bone shape only', 'A'), ('A person has reduced insulin production. Which process is most directly disrupted?', 'Regulation of blood glucose', 'Oxygen exchange', 'Bone movement', 'Sound detection', 'A'), ('Why can damage to the nervous system affect many body functions at once?', 'It coordinates communication and control across many organs', 'It stores all body fat', 'It produces every digestive enzyme', 'It replaces red blood cells', 'A'), ('A blockage prevents blood from reaching a muscle. Why can the muscle lose function?', 'The muscle receives less oxygen and nutrients and cannot remove wastes efficiently', 'The muscle gains too much ATP', 'The lungs stop containing air', 'The bones become hollow immediately', 'A')])]}, {'title': 'Force and Motion', 'topic': 'Force and Motion', 'content': "Motion describes a change in position over time. Speed is the distance traveled per unit time, while velocity includes direction. Acceleration is the rate of change of velocity. A force is a push or pull that can change an object's motion. Newton's first law describes inertia, Newton's second law relates force, mass and acceleration through F = ma, and Newton's third law states that interacting objects exert equal and opposite forces on each other. Friction opposes relative motion between surfaces. Gravity attracts masses toward one another, and near Earth's surface it produces an acceleration of about 9.8 m/s² for freely falling objects when air resistance is neglected.", 'quizzes': [('Easy', [('What is the SI unit of force?', 'Joule', 'Newton', 'Watt', 'Pascal', 'B'), ('What is speed?', 'Distance traveled per unit time', 'Force per unit mass', 'Mass per unit volume', 'Change in direction only', 'A'), ('Which force pulls objects toward Earth?', 'Friction', 'Magnetism', 'Gravity', 'Buoyancy', 'C'), ('What happens when the net force on an object is zero?', 'Its acceleration is zero', 'Its mass becomes zero', 'It must stop immediately', 'Its speed must increase', 'A'), ('Which law is commonly written as F = ma?', "Newton's first law", "Newton's second law", "Newton's third law", 'Law of conservation of energy', 'B')]), ('Medium', [('If the net force on a 2 kg object is 10 N, what is its acceleration?', '2 m/s²', '5 m/s²', '10 m/s²', '20 m/s²', 'B'), ('What does inertia describe?', "An object's resistance to changes in motion", 'The amount of heat in an object', 'The ability to produce light', 'The force of gravity only', 'A'), ('Why does friction usually oppose motion between surfaces?', 'It acts to resist relative sliding or attempted sliding', 'It always increases speed', 'It removes mass', 'It creates gravity', 'A'), ('A car travels 100 m in 5 s. What is its average speed?', '10 m/s', '15 m/s', '20 m/s', '25 m/s', 'C'), ('Which quantity includes both magnitude and direction?', 'Distance', 'Speed', 'Velocity', 'Mass', 'C')]), ('Hard', [('A 4 kg object accelerates at 3 m/s². What net force acts on it?', '0.75 N', '7 N', '12 N', '16 N', 'C'), ('A passenger moves forward when a car suddenly stops. Which concept best explains this?', 'Inertia', 'Buoyancy', 'Radiation', 'Elasticity', 'A'), ('Two skaters push away from each other. Which statement best describes the interaction?', 'Only the heavier skater exerts a force', 'The forces are equal in magnitude and opposite in direction', 'Both exert forces in the same direction', 'No force acts after contact', 'B'), ('If the net force on an object doubles while its mass stays constant, what happens to acceleration?', 'It halves', 'It stays the same', 'It doubles', 'It becomes zero', 'C'), ('Why does a falling object eventually approach a terminal speed in air?', 'Air resistance increases with speed until it balances the downward force', 'Gravity disappears', 'Mass becomes zero', 'The object stops experiencing any forces', 'A')])]}, {'title': 'Matter and Its Properties', 'topic': 'Matter and Its Properties', 'content': 'Matter has mass and occupies space. Common states of matter include solids, liquids and gases. In a solid, particles are closely packed and mainly vibrate around fixed positions. In a liquid, particles can move past one another while remaining relatively close. In a gas, particles are much farther apart and move freely. Temperature is related to the average kinetic energy of particles. Changes of state such as melting, freezing, evaporation, condensation and boiling involve energy transfer without necessarily changing the chemical identity of a substance. Density is mass divided by volume. Physical changes do not create a new substance, whereas chemical changes produce new substances with different properties.', 'quizzes': [('Easy', [('Which state of matter has a fixed shape and fixed volume?', 'Solid', 'Liquid', 'Gas', 'Plasma only', 'A'), ('What is density?', 'Mass divided by volume', 'Volume divided by mass', 'Mass plus volume', 'Temperature divided by mass', 'A'), ('What change turns a liquid into a gas at the surface?', 'Freezing', 'Condensation', 'Evaporation', 'Melting', 'C'), ('Which state generally has particles farthest apart?', 'Solid', 'Liquid', 'Gas', 'Gel', 'C'), ('Which is a physical change?', 'Burning wood', 'Rusting iron', 'Melting ice', 'Digesting food', 'C')]), ('Medium', [('Why can gases be compressed much more easily than solids?', 'Gas particles have much more empty space between them', 'Gas particles have no mass', 'Solid particles do not move', 'Gas particles are always colder', 'A'), ('What happens to the average kinetic energy of particles when temperature increases?', 'It decreases', 'It remains exactly zero', 'It generally increases', 'It becomes mass', 'C'), ('What process changes a gas into a liquid?', 'Sublimation', 'Condensation', 'Melting', 'Freezing', 'B'), ('A substance has a mass of 200 g and a volume of 50 cm³. What is its density?', '2 g/cm³', '4 g/cm³', '10 g/cm³', '250 g/cm³', 'B'), ('Why is boiling different from evaporation?', 'Boiling occurs throughout a liquid at its boiling point, while evaporation occurs at the surface', 'Evaporation only occurs in solids', 'Boiling never involves energy', 'They are chemically different reactions', 'A')]), ('Hard', [('Why does the temperature of a pure substance remain constant during melting under constant pressure?', 'Energy is being used to change the arrangement of particles rather than increase average kinetic energy', 'No energy enters the substance', 'The particles stop moving', 'The mass disappears', 'A'), ('A metal cube sinks in water. What can be concluded if the water and cube are at the same temperature?', 'The cube must have lower density than water', 'The cube has greater density than water', 'The cube has no mass', 'The cube must be a gas', 'B'), ('Which observation is strongest evidence of a chemical change?', 'A solid melts', 'A liquid evaporates', 'A new gas forms during a reaction', 'A substance changes shape', 'C'), ('Why does increasing temperature generally increase gas pressure in a sealed rigid container?', 'Particles move faster and collide with the container walls more frequently and energetically', 'Particles lose all kinetic energy', 'The container becomes larger automatically', 'The gas gains no energy', 'A'), ('A sample contains particles of two different elements chemically bonded together. How should the sample be classified?', 'Mixture', 'Compound', 'Pure element', 'Physical solution only', 'B')])]}, {'title': 'Ecosystems', 'topic': 'Ecosystems', 'content': 'An ecosystem contains living organisms and the nonliving environment with which they interact. Producers such as plants and algae capture energy, usually from sunlight, and form the base of many food chains. Consumers obtain energy by feeding on other organisms, while decomposers break down dead material and return nutrients to the environment. A food chain shows a sequence of energy transfer, while a food web connects many food chains. Energy decreases at higher trophic levels because organisms use much of the energy they obtain for life processes. Matter such as carbon and nitrogen is recycled through ecosystems. Population size is influenced by factors such as food, water, space, predation, disease and climate.', 'quizzes': [('Easy', [('Which organisms are usually producers in an ecosystem?', 'Plants and algae', 'Lions only', 'Fungi only', 'Decomposers only', 'A'), ('What do decomposers do?', 'Produce sunlight', 'Break down dead organic matter', 'Stop nutrient cycles', 'Create predators', 'B'), ('What is a food chain?', 'A sequence showing feeding relationships and energy transfer', 'A list of all weather events', 'A map of soil types', 'A measurement of population age', 'A'), ('Which is a nonliving factor in an ecosystem?', 'Grass', 'Bacteria', 'Temperature', 'Deer', 'C'), ('What is a consumer?', 'An organism that obtains energy by consuming other organisms or organic matter', 'Only a plant', 'Only a decomposer', 'A nonliving factor', 'A')]), ('Medium', [('Why is less energy available at higher trophic levels?', 'Much of the energy is used for metabolism and lost as heat', 'Energy is created at every trophic level', 'Predators never use energy', 'Plants absorb all animal energy', 'A'), ('What is the main role of producers in most food webs?', 'They introduce energy into the biological community by converting light or chemical energy into stored chemical energy', 'They consume all predators', 'They stop decomposition', 'They remove all nutrients', 'A'), ('If a predator population suddenly decreases, what may initially happen to its prey population?', 'It may increase', 'It must immediately disappear', 'It becomes a producer', 'It cannot change', 'A'), ('Why are decomposers important for ecosystems?', 'They recycle nutrients from dead organisms and waste', 'They prevent all organisms from reproducing', 'They remove sunlight', 'They eliminate producers', 'A'), ('What is a food web different from a simple food chain?', 'It represents multiple interconnected feeding relationships', 'It contains no consumers', 'It only includes plants', 'It shows only weather patterns', 'A')]), ('Hard', [('If a disease greatly reduces a plant population, which effect is most likely to occur first in a simple food chain?', 'Herbivores that depend on the plants may decline', 'All decomposers immediately disappear', 'Predators instantly increase', 'Sunlight stops reaching Earth', 'A'), ('Why can removal of a top predator cause changes across several trophic levels?', 'Predators can regulate prey populations, which affects organisms and resources lower in the food web', 'Top predators produce all oxygen', 'Predators are always producers', 'Energy increases at every trophic level', 'A'), ('A lake receives excessive fertilizer runoff and experiences an algal bloom. Why can fish later die?', 'Decomposition of excess organic matter can reduce dissolved oxygen', 'Algae remove all gravity', 'Fish turn into plants', 'Fertilizer directly creates unlimited oxygen', 'A'), ('Why is biodiversity often associated with ecosystem stability?', 'A greater variety of organisms can provide multiple functional roles and alternative responses to disturbance', 'All species perform exactly the same role', 'Biodiversity prevents all environmental change', 'Only predators determine stability', 'A'), ('If energy transfer between trophic levels is inefficient, why must ecosystems generally support fewer organisms at higher trophic levels?', 'Less usable energy is available to support biomass at higher levels', 'Higher trophic levels create energy', 'Higher trophic levels have no metabolism', 'Energy becomes matter and disappears', 'A')])]}]


def seed():
    db = SessionLocal()

    try:
        created_lessons = 0
        created_quizzes = 0
        created_questions = 0

        for lesson_data in LESSONS:
            title = lesson_data["title"]

            lesson = (
                db.query(Lesson)
                .filter(Lesson.title == title)
                .first()
            )

            if lesson is None:
                lesson = Lesson(
                    title=title,
                    topic=lesson_data["topic"],
                    difficulty="MIXED",
                    content=lesson_data["content"],
                )
                db.add(lesson)
                db.flush()
                created_lessons += 1

            for difficulty, questions in lesson_data["quizzes"]:
                quiz_title = f"{title} - {difficulty} Quiz"

                quiz = (
                    db.query(Quiz)
                    .filter(
                        Quiz.lesson_id == lesson.id,
                        Quiz.difficulty == difficulty,
                    )
                    .first()
                )

                if quiz is None:
                    quiz = Quiz(
                        lesson_id=lesson.id,
                        title=quiz_title,
                        difficulty=difficulty,
                    )
                    db.add(quiz)
                    db.flush()
                    created_quizzes += 1

                existing_count = (
                    db.query(Question)
                    .filter(Question.quiz_id == quiz.id)
                    .count()
                )

                if existing_count == 0:
                    for (
                        question_text,
                        option_a,
                        option_b,
                        option_c,
                        option_d,
                        correct_answer,
                    ) in questions:
                        db.add(
                            Question(
                                quiz_id=quiz.id,
                                question=question_text,
                                option_a=option_a,
                                option_b=option_b,
                                option_c=option_c,
                                option_d=option_d,
                                correct_answer=correct_answer,
                            )
                        )
                        created_questions += 1

        db.commit()

        print("Science curriculum seeded successfully.")
        print(f"Lessons created: {created_lessons}")
        print(f"Quizzes created: {created_quizzes}")
        print(f"Questions created: {created_questions}")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed()
