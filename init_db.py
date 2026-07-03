"""
Script d'initialisation de la base de données SQLite.
À lancer une seule fois avant le scraping.
"""
import sqlite3
import os

DB_PATH = "data/rugby.db"

def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS leagues (
            uid TEXT PRIMARY KEY,
            espnId INTEGER NOT NULL,
            name TEXT NOT NULL,
            abbreviationName TEXT NOT NULL,
            season INTEGER NOT NULL,
            startDate TEXT,
            endDate TEXT,
            hasGroups INTEGER,
            hasStandings INTEGER,
            UNIQUE (espnId, season)
        );

        CREATE TABLE IF NOT EXISTS stadiums (
            espnId INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            grass INTEGER,
            indoor INTEGER,
            city TEXT,
            state TEXT
        );

        CREATE TABLE IF NOT EXISTS teams (
            espnId INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            abbreviationName TEXT NOT NULL,
            color TEXT,
            logoUrl TEXT,
            UNIQUE(name)
        );

        CREATE TABLE IF NOT EXISTS standings (
            uid TEXT PRIMARY KEY,
            teamEspnId INTEGER NOT NULL,
            leagueUid TEXT NOT NULL,
            groupId INTEGER,
            gamesPlayed REAL,
            gamesWon REAL,
            gamesLost REAL,
            gamesDrawn REAL,
            gamesBye REAL,
            OTWins REAL,
            OTLosses REAL,
            points REAL,
            pointsFor REAL,
            pointsAgainst REAL,
            pointsDifference REAL,
            avgPointsFor REAL,
            avgPointsAgainst REAL,
            differential REAL,
            triesFor REAL,
            triesAgainst REAL,
            triesDifference REAL,
            rank REAL,
            playoffSeed REAL,
            winPercent REAL,
            divisionWinPercent REAL,
            leagueWinPercent REAL,
            gamesBehind REAL,
            bonusPoints REAL,
            bonusPointsTry REAL,
            bonusPointsLosing REAL,
            streak REAL,
            UNIQUE (teamEspnId, leagueUid),
            FOREIGN KEY (teamEspnId) REFERENCES teams(espnId),
            FOREIGN KEY (leagueUid) REFERENCES leagues(uid)
        );

        CREATE TABLE IF NOT EXISTS matches (
            espnId INTEGER PRIMARY KEY,
            date TEXT NOT NULL,
            name TEXT NOT NULL,
            abbreviationName TEXT NOT NULL,
            leagueUid TEXT,
            homeTeamEspnId INTEGER,
            awayTeamEspnId INTEGER,
            winnerEspnId INTEGER,
            loserEspnId INTEGER,
            stadiumEspnId INTEGER,
            winnerScore INTEGER,
            loserScore INTEGER,
            totalPlayTime REAL,
            UNIQUE(date, name),
            FOREIGN KEY (leagueUid) REFERENCES leagues(uid),
            FOREIGN KEY (homeTeamEspnId) REFERENCES teams(espnId),
            FOREIGN KEY (awayTeamEspnId) REFERENCES teams(espnId),
            FOREIGN KEY (winnerEspnId) REFERENCES teams(espnId),
            FOREIGN KEY (loserEspnId) REFERENCES teams(espnId),
            FOREIGN KEY (stadiumEspnId) REFERENCES stadiums(espnId)
        );

        CREATE TABLE IF NOT EXISTS team_match_stats (
            uid TEXT PRIMARY KEY,
            matchEspnId INTEGER NOT NULL,
            teamEspnId INTEGER NOT NULL,
            opponentEspnId INTEGER,
            linescore1stHalf INTEGER,
            linescore2ndHalf INTEGER,
            linescore20min INTEGER,
            linescore60min INTEGER,
            passes REAL, runs REAL, metres REAL, attackingKicks REAL,
            offload REAL, cleanBreaks REAL, defendersBeaten REAL, breakAssist REAL,
            carriesMetres REAL, carriesCrossedGainLine REAL, carriesNotMadeGainLine REAL,
            carriesSupport REAL, averageGain REAL, dummyHalfMetres REAL,
            hitUps REAL, hitUpMetres REAL, runFromDummyHalf REAL, tackleBusts REAL,
            attackingEventsZoneA REAL, attackingEventsZoneB REAL,
            attackingEventsZoneC REAL, attackingEventsZoneD REAL,
            completeSets REAL, incompleteSets REAL,
            tackles REAL, tackleSuccess REAL, missedTackles REAL,
            turnoverWon REAL, turnoversConceded REAL, turnoverOppHalf REAL,
            turnoverOwnHalf REAL, turnoverLostInRuckOrMaul REAL, turnoverKnockOn REAL,
            turnoverForwardPass REAL, turnoverCarriedInTouch REAL, turnoverCarriedOver REAL,
            turnoverKickError REAL, turnoverBadPass REAL, markerTackles REAL,
            ballWonZoneA REAL, ballWonZoneB REAL, ballWonZoneC REAL, ballWonZoneD REAL,
            points REAL, tries REAL, penaltyTries REAL, tryAssists REAL,
            tryBonusPoints REAL, losingBonusPoints REAL, conversionGoals REAL,
            dropGoalsConverted REAL, dropGoalMissed REAL, goals REAL,
            missedConversionGoals REAL, missedGoals REAL, penaltyGoals REAL,
            missedPenaltyGoals REAL,
            penaltiesConceded REAL, redCards REAL, yellowCards REAL,
            kicks REAL, kickFromHandMetres REAL, kicksFromHand REAL,
            kickChargedDown REAL, kickOutOfPlay REAL, kickInTouch REAL,
            kickOppnCollection REAL, kickPossessionLost REAL, kickPossessionRetained REAL,
            totalKicks REAL, kickPercentSuccess REAL, kickReturns REAL,
            kickReturnMetres REAL, fortyTwenty REAL,
            possession REAL, territory REAL, phaseNumber REAL,
            scrumsWon REAL, scrumsLost REAL, scrumsTotal REAL, scrumsSuccess REAL,
            lineoutsWon REAL, lineoutsLost REAL, totalLineouts REAL, lineoutSuccess REAL,
            rucksWon REAL, rucksLost REAL, rucksTotal REAL, ruckSuccess REAL,
            maulsWon REAL, maulsLost REAL, maulsTotal REAL, maulingMetres REAL,
            maulsWonOutright REAL, maulsWonPenalty REAL, maulsWonPenaltyTry REAL,
            maulsWonTry REAL, maulsLostOutright REAL, maulsLostTurnover REAL,
            ballPossessionLast10Mins REAL, territoryLast10Mins REAL,
            pcPossessionFirst REAL, pcPossessionSecond REAL,
            pcTerritoryFirst REAL, pcTerritorySecond REAL,
            collectionSuccess REAL, collectionFailed REAL, collectionFromKick REAL,
            collectionInterception REAL, collectionLooseBall REAL, handlingError REAL,
            kickSuccess REAL, pcKickPercent REAL, kickPenaltyGood REAL, kickPenaltyBad REAL,
            kickTouchInGoal REAL, kickTryScored REAL, retainedKicks REAL, trueRetainedKicks REAL,
            tryKicks REAL, penaltyKickForTouchMetres REAL,
            freeKickConceded REAL, freeKickConcededAtLineout REAL, freeKickConcededAtScrum REAL,
            freeKickConcededInGeneralPlay REAL, freeKickConcededInRuckOrMaul REAL,
            totalFreeKicksConceded REAL, totalKicksSucceeded REAL,
            lineoutsInfringeOpp REAL, lineoutsInfringeOwn REAL,
            lineoutsToOppPlayer REAL, lineoutsToOwnPlayer REAL,
            lineoutWonOwnThrow REAL, lineoutWonSteal REAL,
            lineoutThrowLostFreeKick REAL, lineoutThrowLostHandlingError REAL,
            lineoutThrowLostNotStraight REAL, lineoutThrowLostOutright REAL,
            lineoutThrowLostPenalty REAL, lineoutThrowNotStraight REAL,
            lineoutThrowWonClean REAL, lineoutThrowWonFreeKick REAL,
            lineoutThrowWonPenalty REAL, lineoutThrowWonTap REAL,
            scrumsLostFreeKick REAL, scrumsLostOutright REAL, scrumsLostPenalty REAL,
            scrumsLostReversed REAL, scrumsReset REAL,
            scrumsWonFreeKick REAL, scrumsWonOutright REAL, scrumsWonPenalty REAL,
            scrumsWonPenaltyTry REAL, scrumsWonPushoverTry REAL, setPieceWon REAL,
            restart22m REAL, restartHalfway REAL,
            restartOwnPlayer REAL, restartOppPlayer REAL, restartOppError REAL,
            restartErrorNotTen REAL, restartErrorOutOfPlay REAL,
            restartsWon REAL, restartsLost REAL, restartsSuccess REAL,
            penaltyConcededCollapsing REAL, penaltyConcededCollapsingMaul REAL,
            penaltyConcededCollapsingOffense REAL, penaltyConcededDelibKnockOn REAL,
            penaltyConcededDissent REAL, penaltyConcededEarlyTackle REAL,
            penaltyConcededFoulPlay REAL, penaltyConcededHandlingInRuck REAL,
            penaltyConcededHighTackle REAL, penaltyConcededKillingRuck REAL,
            penaltyConcededLineoutOffence REAL, penaltyConcededObstruction REAL,
            penaltyConcededOffside REAL, penaltyConcededOppHalf REAL,
            penaltyConcededOther REAL, penaltyConcededOwnHalf REAL,
            penaltyConcededScrumOffence REAL, penaltyConcededStamping REAL,
            penaltyConcededWrongSide REAL,
            won REAL, lost REAL, drawn REAL, numberOfTeams REAL, matches REAL,
            startingMatches REAL, replacementMatches REAL, onReport REAL, playTheBall REAL,
            UNIQUE(matchEspnId, teamEspnId),
            FOREIGN KEY (matchEspnId) REFERENCES matches(espnId),
            FOREIGN KEY (teamEspnId) REFERENCES teams(espnId),
            FOREIGN KEY (opponentEspnId) REFERENCES teams(espnId)
        );

        CREATE TABLE IF NOT EXISTS players (
            espnId INTEGER PRIMARY KEY,
            firstName TEXT,
            lastName TEXT,
            weight REAL,
            height REAL,
            birthDate TEXT,
            birthPlace TEXT,
            positionName TEXT,
            UNIQUE(firstName, lastName, birthDate)
        );

        CREATE TABLE IF NOT EXISTS player_team (
            uid TEXT PRIMARY KEY,
            playerEspnId INTEGER NOT NULL,
            teamEspnId INTEGER NOT NULL,
            season INTEGER,
            UNIQUE (playerEspnId, teamEspnId, season),
            FOREIGN KEY (playerEspnId) REFERENCES players(espnId),
            FOREIGN KEY (teamEspnId) REFERENCES teams(espnId)
        );

        CREATE TABLE IF NOT EXISTS player_match_stats (
            uid TEXT PRIMARY KEY,
            playerTeamUid TEXT NOT NULL,
            matchEspnId INTEGER NOT NULL,
            jersey INTEGER,
            positionName TEXT,
            isFirstChoice INTEGER,
            passes REAL, runs REAL, metres REAL, attackingKicks REAL,
            offload REAL, cleanBreaks REAL, defendersBeaten REAL, breakAssist REAL,
            carriesMetres REAL, gainLine REAL, carriesCrossedGainLine REAL,
            carriesNotMadeGainLine REAL, carriesSupport REAL, averageGain REAL,
            dummyHalfMetres REAL, hitUps REAL, hitUpMetres REAL,
            runFromDummyHalf REAL, tackleBusts REAL,
            tackles REAL, tackleSuccess REAL, missedTackles REAL, markerTackles REAL,
            points REAL, tries REAL, tryAssists REAL, conversionGoals REAL,
            dropGoalsConverted REAL, penaltyGoals REAL,
            penaltiesConceded REAL, redCards REAL, yellowCards REAL,
            kicks REAL, kickMetres REAL, kicksFromHand REAL, kickReturns REAL,
            kickReturnMetres REAL,
            turnoverWon REAL, turnoversConceded REAL,
            minutesPlayedTotal REAL,
            minutesPlayedFirstHalf REAL, minutesPlayedSecondHalf REAL,
            UNIQUE (playerTeamUid, matchEspnId),
            FOREIGN KEY (playerTeamUid) REFERENCES player_team(uid),
            FOREIGN KEY (matchEspnId) REFERENCES matches(espnId)
        );
    """)
    conn.commit()
    conn.close()
    print(f"✅ Base de données initialisée : {DB_PATH}")

if __name__ == "__main__":
    init_db()