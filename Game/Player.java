package Game;

public class Player {
        final String[] HANDS = {"Nothing","High Card", "One Pair", "Three of a Kind", "Two Pair", "Three Pair", "Flush", "Straight", "Straight Flush", "Full House", "Royal Flush"};
        final String DEALEROWNER = "The Deck";
        final String POTOWNER = "The Pot";
        public String name;
        private int handScore;
        private String handName;
        public Player(String name){
            this.name = name;
            this.handScore = 0;
            this.handName = HANDS[this.handScore];
        }

        private void calculateHand(Deck deck){
            this.handScore = deck.scoreHand(this.name);
            this.handName = HANDS[this.handScore];
        }
        public String showHand(Boolean hidden, Deck deck){
            calculateHand(deck);
            if(hidden){
                return deck.showHand(this.name, true);
            }
            return deck.showHand(this.name, false) +": " + this.handName;
        }
        public String showStack(Deck deck){
            return deck.showStack(this.name);
        }
        public void discard(Deck deck){
            String[] selfFilter = {this.name};
            deck.shuffle(selfFilter, DEALEROWNER);
        }
        public void draw(Deck deck, int nTimes){
            String[] DealerFilter = {DEALEROWNER};
            for(int drawn = 0; drawn < nTimes; drawn++){
                deck.giveRandom(DealerFilter, this.name);
            }
        }
        public void drawBet(Deck deck, Boolean pot, int nTimes){
            String[] betFilter = {DEALEROWNER}; 
            if(pot){
                betFilter[0] = POTOWNER;
            }
            for(int drawn = 0; drawn < nTimes; drawn++){
                deck.giveRandom(betFilter, this.name + "s stack");
            }
        }
        public void bet(Deck deck, int nTimes){
            String[] StackFilter = {this.name + "s stack"};
            for(int drawn = 0; drawn < nTimes; drawn++){
                deck.giveRandom(StackFilter, POTOWNER);
            }
        }
        public void burn(Deck deck, int nTimes){
            String[] playerStackFilter = {this.name + "s stack"};
            for(int burnIndex = 0; burnIndex < nTimes; burnIndex++){
                deck.giveRandom(playerStackFilter, this.name);
            }
        }
        public void swap(Deck deck, int index){
            int handNumber = 0;
            for(int deckIndex = 0; deckIndex < deck.cards.length; deckIndex++){
                if(deck.cards[deckIndex].equals(this.name)){
                    if(handNumber == index){
                        deck.cards[deckIndex] = DEALEROWNER;
                        draw(deck, 1);
                        return;
                    }
                    handNumber++;
                }
            }
            System.out.println("not a valid index...");
        }
}

