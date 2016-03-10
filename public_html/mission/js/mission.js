(function(angular) {
  'use strict';

  angular.module('MissionApp',[]);

  function MissionController() {

    var self = this;

var adjectives = Array('Ancient','Bold','Breaking','Brightest','Brilliant','Crescent','Dark|Darkness','Darkest|Darkness','Desert|Desert','Eternal','Evening|Darkness','Final','First','Forever','Giant|Giant','Glorious|Glory','Joyful|Joy','July','Last','Liberty|Liberty','Magic|Magic','Morning|Morning','Power|Power','Phantom','Present','Righteous','Roaring|Roar|Scream','Rolling','Sand','Screaming|Roar|Scream','Silent','Sleeping','Soaring','Standing|Stand','Star|Star','Stunning','Super','Thunderous|Thunder','Twisted','Urgent','Utopian','Valiant');
var nouns = Array('Action','Alert','Bane','Beauty','Claw','Darkness','Dawn','Day','Defense','Desert','Envy','Fall','Fist','Flight','Fury','Guard','Glory','Hammer','Hand','Honor','Hope','Hunt','Hurricane','Joy','Liberty','Light','Lightning','Magic','Morning','October','Power','Rain','Response','Repose','Roar','Scream','Skull','Sky','Skies','Shield','Shout','Stand','Star','Storm','Streak','Strike','Sun','Thunder','Victory','Whisper','Wind','Wrath');
var colors = Array('Black','Blue','Brown','Golden','Gray','Green','Indego','Orange','Purple','Rainbow','Red','Scarlet','Silver','Violet','White','Yellow');
var actors = Array('Cobra','Condor','Dragon','Eagle','Giant','Guardian','Hawk','Hydra','Jackal','King','Knight','Lady','Lion','Scorpion','Spartan','Stranger','Titan','Victor','Viking','Warrior');
var mission_grammars = Array(
    {chance:30, grammar: "{adj1} {noun1}"},
    {chance:20, grammar: "{adj1} {actor}"},
    {chance:10, grammar: "{color} {noun1}"},
    {chance:10, grammar: "{color} {actor}"},
    {chance:20, grammar: "{actor}'s {noun1}"},
    //{chance:10, grammar: "{noun1} of the {noun2}"}, //this one has been producing too many odd lines
    {chance:10, grammar: "{noun1} of the {actor}"},
    {chance:10, grammar: "{actor} of the {noun1}"},
    {chance:5,  grammar: "{noun1} of {noun2}"},
    {chance:5,  grammar: "{noun1} of {color} {noun2}"},
    {chance:10, grammar: "{adj1} {noun1} and {adj2} {noun2}"},
    {chance:3,  grammar: "Attack of the {actor}s"},
    {chance:3,  grammar: "Return of the {actor}s"},
    {chance:1,  grammar: "The {actor} Awakens"}
    );
this.getNoun = function(badNouns) {
  return _.chain(nouns)
    .difference(badNouns)
    .sample()
    .value();
};

this.getMissionName = function() {
  var adj1 = _.sample(adjectives);
  var adj2 = _.sample(adjectives);
  while(adj1 == adj2)
    adj2 = _.sample(adjectives);
  var badWords = _.uniq(adj1.split('|').slice(1).concat(adj2.split('|').slice(1)));
  var noun1 = self.getNoun(badWords);
  var noun2 = self.getNoun(badWords);
  while(noun1 == noun2)
    noun2 = self.getNoun(badWords);
  adj1 = adj1.split('|')[0];
  adj2 = adj2.split('|')[0];
  var color = _.sample(colors);
  var actor = _.sample(actors);

  var mission = '';
  var rand = Math.floor(Math.random() * 100 + 1);
  if(rand <= 25)
    mission += 'Operation ';
  else if(rand <= 50)
    mission += 'Project ';
  else if(rand <= 75)
    mission += 'Code: ';

  var sumChance = _.chain(mission_grammars).pluck('chance').reduce(function(sum, c) { return sum + c;}).value();
  rand = Math.floor(Math.random() * sumChance + 1);
  for(var gi in mission_grammars) {
    var g = mission_grammars[gi];
    if(rand > g.chance) {
      rand -= g.chance;
      }
    else {
      mission += g.grammar
                 .replace(/{adj1}/, adj1)
                 .replace(/{adj2}/, adj2)
                 .replace(/{noun1}/, noun1)
                 .replace(/{noun2}/, noun2)
                 .replace(/{color}/, color)
                 .replace(/{actor}/, actor);
      return mission;
    }
  }
  return '';
};
};

angular.module('MissionApp').controller('MissionController', [MissionController]);
}(window.angular));
