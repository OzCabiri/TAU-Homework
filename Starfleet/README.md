This is a university assignment to implement a program to manage a fleet of spaceships and personnel.

Refer to Starfleet_Hierarchy.pdf for a visual representation of the hierarchy of interfaces and classes.

Interfaces:
  CrewMember, Spaceship

Abstract classes:
  myAbstractCrewMember, myAbstractSpaceship, myAbstractBattleship

Classes:
  Cylon, CrewWoman, Officer, Weapon, TransportShip, Fighter, StealthCruiser, ColonialViper, CylonRaider, Bomber

Enum:
  OfficerRank

Oz Cabiri, June 2023

# Starfleet
A university assignment to implement a program to manage a fleet of spaceships and personnel, in Java.

 Course: Software 1

## Assignment instructions:

### Starfleet Personnel
There are 3 types of Crew-Members:
1. CrewWomen - human crew member.
2. Officer - human crew member, which is an officer.
3. Cylon - cylon crew member. A cylon cannot be an officer.

Services provided by each member:

CrewWomen:
* getName(): returns a unique string representing the crew member's name.
* getAge(): returns the age of the crew member.
* getYearsInService(): returns the number of the crew member's years of service.

Officer:
* includes all services provided by CrewWomen.
* getRank(): returns the officer's rank (represented by an Enum - OfficerRank).

Cylon:
* getName(): returns a unique string representing the crew member's name.
* getAge(): returns the age of the crew member.
* getYearsInService(): returns the number of the crew member's years of service.
* getModelNumber(): returns the cylon's model number (between 1-12, assume correct initialization).

You can ssume that no crew member mans more than 1 ship.

### Starfleet Ships
Spaceship (services provided by all ships):
* getName(): returns a unique string representing the ship's name.
* getCommisionYear(): returns the year of manufacture.
* getMaximalSpeed(): returns the ships's maximal speed (a fraction between 0-10).
* getFirePower(): returns the sum of the ships fire power. Each ship has a base fire power of 10. In combat ships fire power is added from installed weapons.
* getCrewMembers(): returns a set of crew members manning the ship.
* getAnnualMaintanenceCost(): returns the ship's annual maintanence cost.

Transport Ship:
* includes all services provided by Spaceship.
* getCargoCapacity(): returns the ship's cargo capacity.
* getPassengerCapacity(): returns the number of passengers the ship can carry.
* getAnnualMaintanenceCost(): base cost of 3000$. 5$ per megaton of cargo capacity. 3$ per passenger.

Fighter (light combat ship):
* includes all services provided by Spaceship.
* getWeapon(): returns a list of the ship's installed weapons. Each weapon has a name, fire power and maintanence cost.
* getFirePower(): Base fire power + cummulative fire power of all weapons.
* getAnnualMaintanenceCost(): base cost of 2500$. weapons' maintanence cost. engine upkeep (1000*MaximalSpeed, floored).

Fighter (heavy combat ship):
* includes all services provided by Spaceship.
* getWeapon(): returns a list of the ship's installed weapons. Each weapon has a name, fire power and maintanence cost.
* getFirePower(): Base fire power + cummulative fire power of all weapons.
* getNumberOfTechnicians(): returns the number of technicians on the ship (integer between 0-5, does not affect crew size).
* getAnnualMaintanenceCost(): base cost of 5000$. weapons' maintanence cost. each technician reduces the annual cost by 10%.

StealthCruiser (light combat ship):
* includes all services provided by Fighter.
* getAnnualMaintanenceCost(): Fighter's annual cost. stealth engine upkeep (50 * number of stealth engines in the fleet).

ColonialViper (light combat ship):
* includes all services provided by Fighter.
* getAnnualMaintanenceCost(): base cost of 4000$. weapons' maintanence cost. 500% per crew member. engine upkeep (500*MaximalSpeed, floored).

ColonialRaider (light combat ship):
* includes all services provided by Fighter.
* getAnnualMaintanenceCost(): base cost of 3500$. weapons' maintanence cost. 500% per crew member. engine upkeep (1200*MaximalSpeed, floored).