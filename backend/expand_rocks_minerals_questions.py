
import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"
LESSON_TITLE = "Rocks and Minerals"
TARGET_QUESTIONS = 30

# Each question: question, option A, option B, option C, option D, correct answer
QUESTION_BANK = {
    "Easy": [
        ("What are rocks made of?", "One or more minerals", "Only water", "Only air", "Only plant material", "A"),
        ("Which of these is an example of an igneous rock?", "Limestone", "Granite", "Coal", "Chalk", "B"),
        ("Which rock forms when sediments are compacted and cemented?", "Igneous rock", "Metamorphic rock", "Sedimentary rock", "Molten rock", "C"),
        ("Which rock forms when existing rock changes under heat and pressure?", "Sedimentary rock", "Igneous rock", "Volcanic ash only", "Metamorphic rock", "D"),
        ("Which mineral is commonly used in pencil leads?", "Graphite", "Quartz", "Gypsum", "Feldspar", "A"),
        ("Which mineral is commonly used to make glass?", "Talc", "Quartz", "Mica", "Calcite", "B"),
        ("What is magma?", "Solid soil", "A type of fossil", "Molten rock beneath Earth's surface", "A sedimentary layer", "C"),
        ("What is lava?", "Water flowing underground", "A mineral crystal", "Rock formed only by pressure", "Molten rock that reaches Earth's surface", "D"),
        ("Which of these is a sedimentary rock?", "Sandstone", "Granite", "Basalt", "Obsidian", "A"),
        ("Which rock is commonly formed from cooled lava?", "Marble", "Basalt", "Limestone", "Slate", "B"),
        ("What is a mineral?", "Any man-made material", "A mixture of different rocks", "A naturally occurring substance with a characteristic composition and structure", "Only a liquid found underground", "C"),
        ("Which mineral is known for its hardness and use in jewellery?", "Gypsum", "Talc", "Graphite", "Diamond", "D"),
        ("Which of these is a metamorphic rock?", "Marble", "Pumice", "Basalt", "Conglomerate", "A"),
        ("Which rock is often formed from compacted sand grains?", "Granite", "Sandstone", "Marble", "Pumice", "B"),
        ("Which mineral is the main component of limestone?", "Quartz", "Feldspar", "Calcite", "Mica", "C"),
        ("Which rock is often used for kitchen countertops and contains visible crystals?", "Chalk", "Coal", "Shale", "Granite", "D"),
        ("What is a fossil?", "Preserved evidence or remains of ancient life", "A newly formed mineral", "Molten rock", "A type of crystal only", "A"),
        ("Which process breaks rocks into smaller pieces without necessarily moving them?", "Deposition", "Weathering", "Cementation", "Crystallisation", "B"),
        ("What is erosion?", "The formation of magma", "The melting of minerals", "The removal and transport of weathered material", "The transformation of coal into diamond", "C"),
        ("Which rock is commonly used to make statues and sculptures?", "Basalt only", "Pumice only", "Shale only", "Marble", "D"),
        ("Which mineral is commonly found in granite?", "Quartz", "Halite only", "Gypsum only", "Graphite only", "A"),
        ("What is the Mohs scale used to compare?", "Rock age", "Mineral hardness", "Rock temperature", "Mineral colour only", "B"),
        ("Which rock type forms when magma or lava cools and solidifies?", "Sedimentary", "Metamorphic", "Igneous", "Organic soil", "C"),
        ("Which of these is a mineral resource used as fuel?", "Quartz", "Mica", "Calcite", "Coal", "D"),
        ("What is soil partly formed from?", "Weathered rock and organic matter", "Only molten metal", "Only sea water", "Only clouds", "A"),
        ("Which mineral is commonly used in table salt?", "Quartz", "Halite", "Mica", "Talc", "B"),
        ("Which rock is usually lightweight and may float on water because of its many gas pores?", "Marble", "Granite", "Pumice", "Limestone", "C"),
        ("What can the layers in sedimentary rocks sometimes reveal?", "The exact weather tomorrow", "The current temperature of Earth's core", "The number of planets in the Solar System", "Clues about past environments and events", "D"),
        ("Which of these is a common property used to identify minerals?", "Hardness", "A person's age", "The distance to the Moon", "The colour of the sky", "A"),
        ("Why should rocks and minerals be conserved and used responsibly?", "They can all be recreated instantly", "Many resources form very slowly and can be depleted", "They have no practical value", "They exist only in laboratories", "B"),
    ],
    "Medium": [
        ("What is the main difference between a rock and a mineral?", "Every rock is a pure element", "Minerals are always mixtures of rocks", "A mineral has a characteristic composition and structure, while a rock is an aggregate of minerals or other materials", "Rocks are always liquid", "C"),
        ("Which process turns loose sediment into sedimentary rock?", "Melting and freezing only", "Nuclear fusion", "Evaporation of all minerals", "Compaction and cementation", "D"),
        ("Which sequence best represents the formation of many sedimentary rocks?", "Weathering, erosion, deposition, compaction and cementation", "Melting, nuclear fusion, cooling and evaporation", "Pressure, photosynthesis and freezing", "Crystallisation, combustion and rusting", "A"),
        ("How does marble usually form?", "By cooling lava rapidly", "By metamorphism of limestone", "By cementing sand grains", "By freezing seawater", "B"),
        ("Which rock is formed when shale undergoes low-grade metamorphism?", "Granite", "Basalt", "Slate", "Pumice", "C"),
        ("Why do many igneous rocks contain interlocking crystals?", "They are made by plant growth", "Their minerals are glued together by soil", "They form only from compacted fossils", "Minerals crystallise as molten rock cools", "D"),
        ("What generally happens when magma cools slowly underground?", "Larger crystals tend to form", "No minerals can form", "The rock must become sedimentary", "All crystals disappear", "A"),
        ("Which type of igneous rock typically cools quickly at Earth's surface?", "Intrusive", "Extrusive", "Deep mantle rock only", "Metamorphic", "B"),
        ("What is the rock cycle?", "The daily rotation of rocks around Earth", "A process that happens only during earthquakes", "The ongoing transformation of rocks among igneous, sedimentary and metamorphic types", "A method of measuring mineral colour", "C"),
        ("Which conditions are mainly responsible for metamorphism?", "Only sunlight and wind", "Only rainfall", "Only biological decay", "Heat, pressure and chemically active fluids", "D"),
        ("Why is granite usually coarse-grained?", "It commonly cools slowly underground", "It is formed by rapid surface cooling", "It contains no crystals", "It is made entirely of compressed fossils", "A"),
        ("What is the streak of a mineral?", "The sound it makes when struck", "The colour of its powdered form", "Its temperature underground", "Its shape when melted", "B"),
        ("Which test can help distinguish minerals that have similar colours?", "Checking the weather", "Measuring the mineral's distance from Earth", "Testing hardness or streak", "Counting nearby trees", "C"),
        ("What does cleavage describe in a mineral?", "Its ability to burn in air", "Its age in millions of years", "Its magnetic field only", "Its tendency to break along flat planes of weakness", "D"),
        ("What does fracture describe in mineral identification?", "How a mineral breaks when it does not follow cleavage planes", "The mineral's exact age", "The number of atoms in Earth", "The distance between mountains", "A"),
        ("How do fossils most commonly become preserved?", "By turning directly into lava", "Through burial and preservation in suitable conditions", "By exposure to fire for a few seconds", "By dissolving completely in air", "B"),
        ("Why are fossils relatively uncommon in igneous rocks?", "Igneous rocks never occur on land", "Igneous rocks cannot contain minerals", "Heat from molten material usually destroys organic remains", "All igneous rocks are younger than humans", "C"),
        ("Which rock is commonly associated with foliation, or aligned mineral grains, after metamorphism?", "Pumice", "Obsidian", "Conglomerate", "Gneiss", "D"),
        ("What is an ore?", "A naturally occurring material from which a useful substance can be extracted economically", "Any rock found on a beach", "A mineral that dissolves instantly in water", "A rock that contains no useful elements", "A"),
        ("Why are some minerals valuable in electronics?", "They are all transparent", "They may contain elements or have properties useful for electronic components", "They all generate unlimited electricity", "They cannot conduct or respond to energy", "B"),
        ("What is the main difference between weathering and erosion?", "Weathering always transports rock", "Erosion breaks rocks without moving them", "Weathering breaks down material, while erosion removes and transports it", "Both mean only volcanic eruption", "C"),
        ("Which rock is formed from accumulated fragments of other rocks?", "Granite", "Marble", "Quartzite", "Conglomerate", "D"),
        ("How does chemical weathering affect rocks?", "It changes minerals through chemical reactions", "It only moves rocks downhill", "It makes all minerals harder", "It converts every rock into magma immediately", "A"),
        ("Which mineral is the primary ingredient of gypsum plaster?", "Diamond", "Gypsum", "Graphite", "Magnetite", "B"),
        ("What can the presence of rounded pebbles cemented together indicate about a conglomerate?", "It formed only from molten lava", "It is always a metamorphic rock", "Fragments were transported and deposited before becoming cemented", "It contains no sediment", "C"),
        ("Why can limestone react with dilute hydrochloric acid?", "It contains pure iron", "It is made only of quartz", "It contains frozen water", "Its calcite reacts with acid, releasing carbon dioxide", "D"),
        ("What is the typical result when quartz-rich sandstone undergoes metamorphism?", "Quartzite", "Marble", "Slate", "Coal", "A"),
        ("Why are mineral deposits unevenly distributed around Earth?", "All minerals form only in oceans", "Geological processes and conditions vary from place to place", "Every location has identical geology", "Minerals are distributed by the daily weather alone", "B"),
        ("What is mining?", "The natural formation of clouds", "The movement of planets around stars", "The extraction of useful minerals or other geological materials from Earth", "The process of turning all rocks into soil in a laboratory", "C"),
        ("Which practice helps reduce the environmental impact of mining?", "Dumping waste into rivers", "Removing all vegetation without restoration", "Leaving unstable excavations unmanaged", "Rehabilitating mined land and managing waste responsibly", "D"),
    ],
    "Hard": [
        ("An igneous rock has large, visible crystals. What does this most strongly suggest?", "The magma cooled slowly, allowing crystals to grow", "The lava cooled instantly", "The rock formed only from compressed fossils", "The rock contains no minerals", "A"),
        ("A rock contains rounded pebbles cemented within a finer matrix. Which rock is it most likely to be?", "Marble", "Conglomerate", "Gneiss", "Obsidian", "B"),
        ("Which transformation can occur when limestone is subjected to heat and pressure?", "Limestone becomes basalt by melting and surface cooling", "Limestone becomes coal through ordinary weathering", "Limestone recrystallises into marble", "Limestone turns into pure quartz without any geological change", "C"),
        ("Why can a metamorphic rock show foliation?", "All minerals dissolve completely", "It forms only through rapid cooling of lava", "Sediment is always rounded by rivers", "Minerals become aligned under directed pressure during metamorphism", "D"),
        ("Which process most directly forms an intrusive igneous rock?", "Magma solidifies beneath Earth's surface", "Sediment is cemented on a riverbed", "Limestone recrystallises without melting", "Sand grains are transported by wind", "A"),
        ("A mineral scratches calcite but is scratched by quartz. What can be inferred from the Mohs scale?", "Its hardness is below 1", "Its hardness is greater than calcite's but less than quartz's", "Its hardness is greater than diamond's", "Its hardness is exactly 10", "B"),
        ("Which rock is most likely to preserve delicate fossils?", "Fresh basalt", "Obsidian", "Fine-grained sedimentary rock deposited under suitable conditions", "Granite formed deep underground", "C"),
        ("Why does obsidian generally lack visible mineral crystals?", "It forms by cementing sand grains", "It contains only fossil fragments", "It is always a metamorphic rock", "It cools so rapidly that crystals have little time to grow", "D"),
        ("Which statement about the rock cycle is correct?", "Any rock type can be transformed into another through suitable geological processes", "Every rock must pass through magma in every cycle", "Metamorphic rocks cannot be weathered", "Sedimentary rocks can never undergo heat or pressure", "A"),
        ("Which mineral property describes the way a mineral reflects light from its surface?", "Streak", "Lustre", "Cleavage", "Specific gravity", "B"),
        ("A mineral has a hardness of 7 on the Mohs scale. Which common mineral is closest to that hardness?", "Talc", "Gypsum", "Quartz", "Calcite", "C"),
        ("Which sequence best describes the formation of quartzite from sandstone?", "Cooling of magma, then deposition", "Compaction of lava, then evaporation", "Weathering, then melting into metal", "Burial and metamorphism causing quartz grains to recrystallise and interlock", "D"),
        ("Why can the same mineral occur in rocks of different types?", "Minerals can form under different geological conditions and become part of different rocks", "Each mineral can exist in only one rock type", "Minerals are created only by plants", "Rock type is determined entirely by colour", "A"),
        ("Which condition most strongly promotes contact metamorphism?", "Sediment settling in still water", "Hot magma heating surrounding country rock", "Wind transporting sand across a desert", "A river rounding pebbles", "B"),
        ("What is regional metamorphism commonly associated with?", "Only the freezing of ocean water", "Only surface erosion", "Large-scale heat and pressure during tectonic processes", "The rapid cooling of lava at the surface", "C"),
        ("Why can slate split into thin sheets?", "It contains large rounded pebbles", "It formed only from lava", "It has no mineral alignment", "Low-grade metamorphism produces closely spaced cleavage planes", "D"),
        ("Which statement best distinguishes magma from lava?", "Magma is molten rock below the surface; lava is molten rock that reaches the surface", "Magma is solid rock and lava is liquid water", "Magma is sediment and lava is a mineral", "They are always chemically unrelated substances", "A"),
        ("A rock is made of interlocking quartz and feldspar crystals and has no layering. Which origin is most likely?", "Recent river deposition", "Igneous crystallisation", "Accumulation of shells only", "Low-grade metamorphism of shale only", "B"),
        ("Which property is especially useful for identifying magnetite?", "Taste", "Smell", "Magnetic behaviour", "Transparency alone", "C"),
        ("Why is mineral streak sometimes more reliable than surface colour?", "Streak measures the mineral's age", "Streak reveals the exact place it formed", "Surface colour never changes", "Surface impurities or weathering can change apparent colour while powdered streak may remain characteristic", "D"),
        ("Which statement about coal is most accurate?", "It is a sedimentary rock formed mainly from accumulated and altered plant material", "It is an igneous rock formed from cooled lava", "It is a pure metallic mineral", "It is formed by the rapid cooling of magma", "A"),
        ("What geological process can expose deeply formed metamorphic rocks at Earth's surface?", "Nuclear fusion", "Uplift and erosion", "Photosynthesis", "Condensation of atmospheric water only", "B"),
        ("Why may limestone develop caves in regions with suitable groundwater?", "Limestone is always hollow when formed", "Limestone melts at room temperature", "Slightly acidic water can dissolve calcite over time", "All limestone is made of salt crystals", "C"),
        ("Which observation would best support the interpretation that a rock formed from volcanic lava?", "It contains only large fossils", "It consists of cemented rounded pebbles", "It shows mineral alignment from regional pressure", "It has a fine-grained or glassy texture consistent with rapid surface cooling", "D"),
        ("What is the primary geological significance of unconformities in rock layers?", "They can indicate gaps in the geological record caused by erosion or non-deposition", "They prove all layers formed simultaneously", "They indicate that no geological changes occurred", "They measure mineral hardness", "A"),
        ("Which factor can influence the size of crystals in igneous rocks?", "The number of nearby rivers only", "Cooling rate of the molten material", "The current weather alone", "The number of fossils in the rock", "B"),
        ("Why can a rock's mineral composition help identify its formation history?", "All rocks contain exactly the same minerals", "Minerals cannot change under geological conditions", "Minerals form and remain stable under particular physical and chemical conditions", "Mineral composition depends only on the rock's colour", "C"),
        ("Which process can turn loose sand into sandstone?", "Melting and rapid cooling", "Regional metamorphism alone", "Nuclear fusion", "Compaction and cementation", "D"),
        ("Which statement best describes a renewable versus non-renewable geological resource?", "Many mineral deposits form over geological timescales and are effectively non-renewable on human timescales", "Every mineral deposit replenishes within a few days", "All rocks are renewable in a human lifetime", "Non-renewable resources never occur naturally", "A"),
        ("Why is recycling metals an important part of sustainable resource use?", "It makes metal deposits grow underground", "It can reduce demand for newly mined ore and lower some environmental impacts", "It turns all waste into renewable energy", "It eliminates every environmental impact of mining", "B"),
    ],
}


def normalize(text):
    return " ".join(text.lower().split())


def main():
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DATABASE_PATH}")

    conn = sqlite3.connect(DATABASE_PATH)

    try:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id FROM lessons WHERE LOWER(TRIM(title)) = LOWER(TRIM(?))",
            (LESSON_TITLE,),
        )
        lesson_rows = cursor.fetchall()

        if len(lesson_rows) != 1:
            raise RuntimeError(
                f"Expected exactly one lesson named '{LESSON_TITLE}', "
                f"but found {len(lesson_rows)}."
            )

        lesson_id = lesson_rows[0][0]
        total_added = 0

        for difficulty in ("Easy", "Medium", "Hard"):
            cursor.execute(
                """
                SELECT id FROM quizzes
                WHERE lesson_id = ?
                  AND LOWER(TRIM(difficulty)) = LOWER(TRIM(?))
                """,
                (lesson_id, difficulty),
            )
            quiz_rows = cursor.fetchall()

            if len(quiz_rows) != 1:
                raise RuntimeError(
                    f"Expected exactly one {difficulty} quiz for "
                    f"'{LESSON_TITLE}', but found {len(quiz_rows)}."
                )

            quiz_id = quiz_rows[0][0]

            cursor.execute(
                "SELECT question FROM questions WHERE quiz_id = ?",
                (quiz_id,),
            )
            existing_questions = {
                normalize(row[0]) for row in cursor.fetchall()
            }

            cursor.execute(
                "SELECT COUNT(*) FROM questions WHERE quiz_id = ?",
                (quiz_id,),
            )
            current_count = cursor.fetchone()[0]

            needed = max(0, TARGET_QUESTIONS - current_count)
            unique_candidates = []
            seen = set()

            for item in QUESTION_BANK[difficulty]:
                key = normalize(item[0])

                if key not in existing_questions and key not in seen:
                    unique_candidates.append(item)
                    seen.add(key)

            if len(unique_candidates) < needed:
                raise RuntimeError(
                    f"{difficulty}: need {needed} new questions, "
                    f"but only {len(unique_candidates)} unique questions "
                    "are available. No changes have been committed."
                )

            to_insert = unique_candidates[:needed]

            cursor.executemany(
                """
                INSERT INTO questions
                (quiz_id, question, option_a, option_b, option_c,
                 option_d, correct_answer)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        quiz_id,
                        question,
                        option_a,
                        option_b,
                        option_c,
                        option_d,
                        answer,
                    )
                    for (
                        question,
                        option_a,
                        option_b,
                        option_c,
                        option_d,
                        answer,
                    ) in to_insert
                ],
            )

            total_added += len(to_insert)

            cursor.execute(
                "SELECT COUNT(*) FROM questions WHERE quiz_id = ?",
                (quiz_id,),
            )
            final_count = cursor.fetchone()[0]

            print(
                f"{difficulty}: started with {current_count}, "
                f"added {len(to_insert)}, final total {final_count}"
            )

        conn.commit()
        print(
            f"\nSuccess! Added {total_added} questions "
            f"to '{LESSON_TITLE}'."
        )
        print("Other lessons and Social Science were not modified.")

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


if __name__ == "__main__":
    main()
