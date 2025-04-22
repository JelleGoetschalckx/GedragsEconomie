#_____________________________________GEDRAGSECONOMIE_SCRIPT_____________________________________#
"""
Gemaakt door Jelle Goetschalckx en Mila Cortoos - Laatste bewerking op 7/04/2025
"""
#________________________________________________________________________________________________#

from psychopy import visual, event, core, data, gui
import os, random

def participant_info(directory):
    """
    GUI-box vraagt gegevens participant
    :param directory: plaats waar savefile komt, nodig om te controleren of filenaam al bestaat
    :return: nummer, gender en leeftijd van de participant + wie experiment begeleide
    """
    # (gender en onderzoeker opties apart, anders geen dropdown-menu als incomplete info gegeven → reset nodig)
    gender_opties = ["Maak je keuze", "Man", "Vrouw", "Andere/Zeg ik liever niet"]
    onderzoeker_opties = ["Maak je keuze", "Jelle", "Mila", "Lola", "Simon", "Sophie", "Testmodus"]  # alfabetisch bepaald

    info = {
        "Gender" : gender_opties,
        "Leeftijd": "",
        "Onderzoeker": onderzoeker_opties,
    }

    # Vraag info, herhaal zolang niet alles ingevuld is of het nummer al gebruikt werd
    while (info["Gender"] == gender_opties[0] or
           not info["Leeftijd"] or
           info["Onderzoeker"] == onderzoeker_opties[0]):

        # Waarden resetten als geen antwoord gegeven
        if info["Gender"] == gender_opties[0]:
            info["Gender"] = gender_opties

        if info["Onderzoeker"] == onderzoeker_opties[0]:
            info["Onderzoeker"] = onderzoeker_opties

        info_box = gui.DlgFromDict(dictionary=info, title="Vul hier wat informatie in voor je begint",
                                   order = ["Nummer", "Leeftijd", "Gender", "Onderzoeker"])
        # Stop experiment als er op "cancel" wordt geduwd
        if not info_box.OK:
            core.quit()

    # Bepaal laagste nummer dat nog niet gebruikt werd
    laagste_nummer_gevonden = False
    part_nummer = 1
    while not laagste_nummer_gevonden:
        if not os.path.exists(f"{directory}_{info['Onderzoeker']}_{part_nummer}.csv"):
            laagste_nummer_gevonden = True
        else:
            part_nummer += 1

    return info["Gender"], info["Leeftijd"], str(info["Onderzoeker"]).lower(), part_nummer

class Stimuli:
    def __init__(self, win, condities):
        self.condities = condities

        # Vazen
        tekenpunten_vaas_links = [[-0.4, 0.75], [-0.4, 0.5], [-0.2, 0.25], [-0.15, 0], [-0.15, -0.25], [-0.2, -0.5],
                                  [-0.3, -0.75], [-0.7, -0.75], [-0.8, -0.5], [-0.85, -0.25], [-0.85, 0], [-0.8, 0.25],
                                  [-0.6, 0.5],[-0.6, 0.75]]
        tekenpunten_vaas_rechts = [[0.4, 0.75], [0.4, 0.5], [0.2, 0.25], [0.15, 0], [0.15, -0.25], [0.2, -0.5],
                                   [0.3, -0.75], [0.7, -0.75], [0.8, -0.5], [0.85, -0.25], [0.85, 0], [0.8, 0.25],
                                   [0.6, 0.5], [0.6, 0.75]]

        self.vaas1 = visual.ShapeStim(win, lineColor='black', lineWidth=5, vertices=tekenpunten_vaas_links)
        self.vaas2 = visual.ShapeStim(win, lineColor='black', lineWidth=5, vertices=tekenpunten_vaas_rechts)

        # FixCross
        self.fix_cross = visual.TextStim(win, text="+", color="black")
        # Basic ball met alle mogelijke posities in vaas
        self.bal = visual.Circle(win, size=(0.045, 0.08), pos=(-0.5, -0.25), color='white')
        self.alle_posities = self.gridmaker()

        # TextStims
        self.tekst_vaas1 = visual.TextStim(win)
        self.tekst_vaas2 = visual.TextStim(win)
        self.vaas1_titel = visual.TextStim(win, text="Vaas 1", pos=(-0.5, 0.1))
        self.vaas2_titel = visual.TextStim(win, text="Vaas 2", pos=(0.5, 0.1))

    @staticmethod
    def gridmaker() -> list:
        """
        Maak alle mogelijke posities van bal in vaas in volgorde
        :return: tuple van alle posities
        """
        balpos = [(-0.675, -0.65, 8), (-0.7, -0.55, 9), (-0.75, -0.45, 11), (-0.775, -0.35, 12), (-0.775, -0.25, 12),
                  (-0.8, -0.15, 13), (-0.8, -0.05, 13), (-0.775, 0.05, 12), (-0.75, 0.15, 11)]
        alle_posities = []
        for positie in balpos:
            for i in range(positie[2]):
                alle_posities.append((round(positie[0] + i * 0.05, 4), positie[1]))
        return alle_posities

    def teken(self, current_trial, meeste_rood):
        """
        Teken ballen op scherm, random links of rechts meerderheid
        :param current_trial: geef TrialHandler trial door, condities en proporties worden gebruikt
        :param meeste_rood: moet links of rechts meeste rood (in verhouding) bevatten?
        :return:
        """
        # Extract hoeveel rode en hoeveel totaal, links en rechts
        rood_vaas1 = current_trial['proporties'][0][0]
        rood_vaas2 = current_trial['proporties'][1][0]
        totaal_vaas1 = current_trial['proporties'][0][1]
        totaal_vaas2 = current_trial['proporties'][1][1]

        # Teken fix_cross
        self.fix_cross.draw()

        # Teken verbale stim als conditie 'tekst' is
        if current_trial["conditie"] == self.condities[0]: # als tekst trial
            self.tekst_vaas1.text = f"{totaal_vaas1} ballen waarvan {rood_vaas1} rode"
            self.tekst_vaas2.text = f"{totaal_vaas2} ballen waarvan {rood_vaas2} rode"
            self.tekst_vaas1.pos = (-0.5, -0.1) if meeste_rood == 'links' else (0.5, -0.1)
            self.tekst_vaas2.pos = (-0.5, -0.1) if meeste_rood == 'rechts' else (0.5, -0.1)

            self.vaas1_titel.draw()
            self.vaas2_titel.draw()
            self.tekst_vaas1.draw()
            self.tekst_vaas2.draw()

        # Of teken visuele stim als conditie visueel is
        else:
            self.vaas1.draw()
            # Sample evenveel posities van lijst als aantal ballen die getekend moeten worden
            ballen_vaas1_pos = self.alle_posities[:totaal_vaas1]
            # Randomize posities, zodat rood/wit random verspreid geraken
            random.shuffle(ballen_vaas1_pos)
            for i1, positie in enumerate(ballen_vaas1_pos):
                self.bal.pos = (abs(positie[0]), positie[1]) if meeste_rood == "rechts" else (positie[0], positie[1])
                self.bal.color = "red" if i1 < rood_vaas1 else "white"
                self.bal.draw()

            # Idem voor vaas2, maar dan omgekeerd
            self.vaas2.draw()
            ballen_vaas2_pos = self.alle_posities[:totaal_vaas2]
            random.shuffle(ballen_vaas2_pos)
            for i2, positie in enumerate(ballen_vaas2_pos):
                self.bal.pos = (abs(positie[0]), positie[1]) if meeste_rood == "links" else (positie[0], positie[1])
                self.bal.color = "red" if i2 < rood_vaas2 else "white"
                self.bal.draw()


class Experiment:
    def __init__(self, tijd_conditie, tijd_response, proporties):
        self.condities = ["tekst8", 2, 8]  # hardcode cijfer bij "tekst" (i know, ugly)
        self.proporties = proporties

        self.tijd_conditie = tijd_conditie
        self.tijd_response = tijd_response

        # Bepaal opslagplek
        self.directory = directory = os.path.join(os.getcwd(), 'gedragseconomie_data_', 'participant')
        # Vraag info op
        self.gender, self.leeftijd, self.onderzoeker, self.part_nummer = participant_info(self.directory)
        # Maak ExperimentHandler, save als CSV met participant nummer achteraan
        self.exp_data = data.ExperimentHandler(dataFileName=f"{directory}_{self.onderzoeker}_{self.part_nummer}")

        # Maak win (& hide muis), maak instance van Stimuli class, message template en eindscore counter
        self.win = visual.Window(fullscr=True)
        self.win.mouseVisible = False
        self.stimuli = Stimuli(win=self.win, condities=self.condities)
        self.bericht = visual.TextStim(self.win, height=0.08)
        self.eindscore = 0

    #______TEXT_STIMS______#
    def communicatie(self, sleutelwoord, spatie_duwen=True, wachttijd=0) -> None:
        """
        Geef tekst weer op het scherm
        :param sleutelwoord: dict zet kort woord om in lange versie van tekst (vermijdt in-code clutter)
        :param spatie_duwen: True als participant op spatie moet duwen om verder te gaan, False als automatisch doorgaan
        :param wachttijd: tijd dat bericht op scherm blijft als spatie_duwen=False
        :return:
        """
        opties = {
            "informed_consent": f"GEÏNFORMEERDE TOESTEMMING\n{'_'*25}\n\n"
                                "Ik verklaar dat ik volledig vrijwillig deelneem aan het onderzoek.\n\n"
                                "Ik geef de toestemming aan de proefleiders om mijn resultaten op anonieme wijze te "
                                "bewaren, te verwerken en te rapporteren.\n\n"
                                "Ik ben op de hoogte van de mogelijkheid om mijn deelname aan het onderzoek op ieder "
                                "moment stop te zetten.\n\n"
                                "Duw op spatie om te bevestigen of duw op esc om te weigeren.",
            "intro": "Welkom bij dit experiment!\n\nZo meteen krijg je telkens de keuze tussen twee vazen die gevuld zijn "
                     "met ballen. De meeste ballen zijn wit, sommigen zijn rood. Jouw taak is om bij elke keuze de vaas te "
                     "kiezen waaruit je het liefst blind een bal zou laten trekken als je graag een rode bal wilt krijgen.\n\n"
                     "Met andere woorden: kies de vaas waarvan jij denkt dat je de meeste kans hebt om een rode bal te "
                     "trekken.\n\nDuw op spatie voor verdere instructies.",
            "meer_info": "\nSoms worden de vazen in tekstvorm voorgesteld en soms zijn ze getekend, jouw taak blijft steeds dezelfde. "
                         "In het begin van elke ronde krijg je te zien hoeveel tijd je hebt.\n\n"
                         "Als je de linkse vaas wilt kiezen, duw je op 'f' en voor de rechtse vaas duw je op 'j'\n\nEerst "
                         "zie je de opties, daarna moet je snel antwoord geven.\n\n"
                         "Duw op spatie om dit kort te oefenen.",
            "practice_correct": "Correct!",
            "practice_fout": "Fout!",
            "practice_traag": "Te traag!",
            "begin_echt_exp": "De oefenronde is voorbij, nu begint het echte experiment.\n\nDuw op spatie om te beginnen",
            self.condities[0]: "Tekst: denk goed na!",
            self.condities[1]: "Kort: beslis snel!",
            self.condities[2]: "Lang: denk goed na!",
            "antwoord": "Antwoord nu!",
            "einde": f"Dit is het einde van het experiment.\nJe hebt de juiste keuze gemaakt in {self.eindscore} van de "
                     f"30 gevallen.\n\nBedankt om deel te nemen!\n"
                     f"Duw op spatie om af te sluiten."
        }
        self.bericht.text = opties[sleutelwoord]
        self.bericht.draw()
        self.win.flip()
        if spatie_duwen:
            if event.waitKeys(keyList=["space", "escape"])[0] == "escape":
                core.quit()
        elif wachttijd:
            core.wait(wachttijd)

    #______TRIAL_CREATION______#
    def trial_maker(self) -> tuple:
        """
        Maakt alle trials aan, zowel practice als main exp trials
        :return: oefen-trials en exp trials
        """
        # Maak practice trials
        practice_trial_list = data.createFactorialTrialList({
            "proporties": [((1, 2), (1, 3))],
            "conditie": self.condities
        })
            # hier geen TrialHandler, doet practice_trial_runner zelf (onbepaald aantal iteraties)

        # Maak main trials
        trial_list = data.createFactorialTrialList({
            "proporties": self.proporties,
            "conditie": self.condities
        })
        self.reshuffle_no_consecutives(trial_list)
        exp_trials = data.TrialHandler(trial_list, nReps=2, method="random")
        self.exp_data.addLoop(exp_trials)

        return practice_trial_list, exp_trials

    def reshuffle_no_consecutives(self, trials):
        solved = False
        while not solved:
            random.shuffle(trials)
            if self.no_consecutives(trials):
                solved = True

    @staticmethod
    def no_consecutives(trials):
        for i in range(len(trials)):
            if trials[i]["proporties"] == trials[i - 1]["proporties"] and i != 0:
                return False
        return True

    #______TRIAL_RUNNERS______#
    def practice_trial_runner(self) -> None:
        """
        Runs oefen-trials, herhaalt totdat 3 achter elkaar correct zijn (zeker zijn dat PP opdracht begrijpt)
        :return: None
        """
        juist_counter = 0
        while juist_counter < 3:
            juist_counter = 0

            # maak nieuwe trials in de loop zelf, anders zijn er te weinig bij iteratie
            practice_trials_list, _ = self.trial_maker()
            practice_trials = data.TrialHandler(practice_trials_list, nReps=1, method="sequential")

            for practice_trial in practice_trials:
                # toon welke conditie
                self.communicatie(practice_trial["conditie"], spatie_duwen=False, wachttijd=self.tijd_conditie)

                # toon trial en geef tijd om te antwoorden (random links/rechts bij oefenen)
                kant_meeste_rood_practice = random.sample(['links', 'rechts'], 1)[0]
                self.stimuli.teken(practice_trial, kant_meeste_rood_practice)

                self.win.flip()
                core.wait(int(self.condities[0][-1] if practice_trial["conditie"] == self.condities[0] else practice_trial["conditie"]))

                self.communicatie("antwoord", spatie_duwen=False)

                # wacht op response
                response = event.waitKeys(keyList=["f", "j", "escape"],
                                          maxWait=self.tijd_response)  # x sec tijd om te antwoorden
                if response:
                    response = response[0]
                    if response == "escape":
                        core.quit()

                    accuracy = (kant_meeste_rood_practice == "rechts" and response == "j") or (
                                kant_meeste_rood_practice == "links" and response == "f")
                    # in practice trials wel info geven over hoe accuraat
                    if accuracy:
                        self.communicatie("practice_correct", spatie_duwen=False, wachttijd=1)
                        juist_counter += 1
                    else:
                        self.communicatie("practice_fout", spatie_duwen=False, wachttijd=1)
                else:
                    self.communicatie("practice_traag", spatie_duwen=False, wachttijd=1)

                # maak scherm terug leeg en geef volgende stim (even rust want gaat anders te snel)
                self.stimuli.fix_cross.draw()
                self.win.flip()
                core.wait(1)

    def trial_runner(self, trials) -> None:
        """
        Run main experiment
        :param trials: alle TrialHandler trials die uitgevoerd moeten worden
        :return: None
        """
        for trial in trials:
            # bepaal random welke kant minste ballen krijgt
            kant_meeste_rood = random.sample(["rechts", "links"], 1)[0]

            # toon welke conditie
            self.communicatie(trial["conditie"], spatie_duwen=False, wachttijd=self.tijd_conditie)

            # toon trial en geef tijd om te antwoorden
            self.stimuli.teken(trial, kant_meeste_rood)

            self.win.flip()
            core.wait(int(self.stimuli.condities[0][-1] if trial["conditie"] == self.stimuli.condities[0] else trial["conditie"]))
            # onhandige poging om tijd te hardcoden samen met tekst

            self.communicatie("antwoord", spatie_duwen=False)

            response = event.waitKeys(keyList=["f", "j", "escape"], maxWait=self.tijd_response)

            if response:
                response = response[0]
                if response == "escape":
                    core.quit()
            else:
                response = "g/a"

            # correct antwoord wanneer minderheid aangeduid als meer rode ballen
            accuracy = (kant_meeste_rood == "rechts" and response == "j") or (
                        kant_meeste_rood == "links" and response == "f")
            if accuracy:
                self.eindscore += 1

            if self.onderzoeker != "testmodus":
                trials.addData("juist_kant", kant_meeste_rood)
                trials.addData("juiste_response", "f" if kant_meeste_rood == "links" else "j")
                trials.addData("response", response)
                trials.addData("accuracy", int(accuracy) if response != "g/a" else "g/a")
                trials.addData("leeftijd", self.leeftijd)
                trials.addData("gender", self.gender)
                trials.addData("nummer", self.part_nummer)
                self.exp_data.nextEntry()

            # maak scherm terug leeg en geef volgende stim (even rust want gaat anders te snel)
            self.stimuli.fix_cross.draw()
            self.win.flip()
            core.wait(1)

    #______MAIN______#
    def main(self) -> None:
        """
        Run het experiment in volgorde
        :return: None
        """
        # Informed consent
        self.communicatie("informed_consent")
        # Introductie messages
        self.communicatie("intro")
        self.communicatie("meer_info")

        # Maak trials aan
        practice_trials, exp_trials = self.trial_maker()

        # Run practice trials
        self.practice_trial_runner()

        # Kondig experiment aan en run
        self.communicatie("begin_echt_exp")
        self.trial_runner(exp_trials)

        # Geef salute en quit
        self.communicatie("einde")
        core.quit()

if __name__ == "__main__":
    Experiment(
        tijd_conditie=3,
        tijd_response=3,
        proporties = [((1, 10), (8, 100)), ((1, 8), (8, 80)), ((2, 12), (10, 75)), ((1, 10), (5, 60)), ((2, 8), (10, 50))]
    ).main()
