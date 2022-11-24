package Game;

import java.util.Random;
import java.util.Arrays;
import java.util.ArrayList;

public class Deck {
        final String[] SUITS = {"♥","♦","♠","♣"};
        final String[] VALUES = {"A","2","3","4","5","6","7","8","9","T","J","Q","K"};
        final String DEALEROWNER = "The Deck";
        final String POTOWNER = "The Pot";
        public String[] cards; 
        private Random selector;
        public Deck(){
            this.cards = new String[52];
            Arrays.fill(this.cards, DEALEROWNER);
            this.selector = new Random();
        }
        private String indexToCard(int index){
            if(index > this.cards.length || index < 0){
                System.out.println("Invalid card index, providing joker");
                return "🃟";
            }
            String suit = SUITS[((index) / 13)];
            String value = VALUES[((index) % 13)];
            return "[" + value + suit + "]";
        }
        private int indexToValue(int index){
            return ((index) % 13);
        }
        private int indexToSuit(int index){
            return ((index) / 13);
        }
        public int scoreHand(String owner){
            int score = 0;
            int[] values = new int[13];
            Arrays.fill(values, 0);
            int[] royals = {0,0,0,0};
            int[] suit_totals = {0,0,0,0};
            int streak = 0;
            boolean straight = false;
            boolean highcard = false;
            boolean onepair = false;
            boolean twopair = false;
            boolean threekind = false;
            boolean flush = false;
            boolean threepair = false;
            boolean fullhouse = false;
            for(int deckIndex = 0; deckIndex < this.cards.length; deckIndex++){
                if(this.cards[deckIndex].equals(owner)){
                    int value = indexToValue(deckIndex);
                    int suit =  indexToSuit(deckIndex);
                    values[value]++;
                    suit_totals[suit]++;
                    if(value == 11){
                        royals[1]++;
                    }
                    if(value == 12){
                        royals[2]++;
                    }
                    if(value == 0){
                        royals[3]++;
                    }
                    if(value == 1){
                        royals[0]++;
                    }
                }
            }
            int pairs = 0;
            for(int streakIndex = 0; streakIndex < values.length; streakIndex++){
                if(streak >= 5){
                    straight = true;
                }
                if(values[streakIndex] > 0){
                    if(streakIndex >= 10){
                        highcard = true;
                    }
                    if(values[streakIndex] == 2){
                        onepair = true;
                        pairs++;
                        if(pairs == 2){
                            twopair = true;
                        }
                        if(pairs == 3){
                            threepair = true;
                        }
                    }
                    if(values[streakIndex] == 3){
                        threekind = true;
                    }
                    streak++;
                }
                else{
                    streak = 0;
                }
            }
            for(int suitIndex = 0; suitIndex < suit_totals.length; suitIndex++){
                if(suit_totals[suitIndex] > 5){
                    flush = true;
                }
            }
            int royalSum = 0;
        
            for(int royalIndex = 0; royalIndex < royals.length; royalIndex++){
                royalSum += royals[royalIndex];
                if(royalSum >= 5){
                    fullhouse = true;
                }
            }
            if(highcard){
                score = 1;
            }
            if(onepair){
                score = 2;
            }
            if(threekind){
                score = 3;
            }
            if(twopair){
                score = 4;
            }
            if(threepair){
                score = 5;
            }
            if(flush){
                score = 6;
            }
            if(straight){
                score = 7;
            }
            if(straight && flush){
                score = 8;
            }
            if(fullhouse){
                score = 9;
            }
            if(flush && fullhouse){
                score = 10;
            }
            return score;
        }

        public String showStack(String owner){
            ArrayList<String> stack = new ArrayList<String>();
            for (int deckIndex = 0; deckIndex < this.cards.length; deckIndex++) {
                if(this.cards[deckIndex].equals(owner + "s stack")){
                        if(stack.size() == 0){
                            stack.add("[##]");
                        }
                        stack.add("]");
                    }
            }
            stack.add(owner + "s stack: " + stack.size());
            return stack.toString().replace(",", ""); 
        }

        public String showHand(String owner, Boolean hidden){
            ArrayList<String> hand = new ArrayList<String>();
            for (int deckIndex = 0; deckIndex < this.cards.length; deckIndex++) {
                if(this.cards[deckIndex].equals(owner)){
                    if(!hidden){
                        hand.add(indexToCard(deckIndex));
                    }
                    else{
                        hand.add("[##]");
                    }
                }
            }
            hand.add(owner + "s hand");
            return hand.toString().replace(",", ""); 
        }

        public void giveCard(int index, String newOwner){
            this.cards[index] = newOwner;
        }
        public void giveRandom(String[] filter, String newOwner){
            ArrayList<Integer> filteredIndexes = new ArrayList<Integer>();
            for (int deckIndex = 0; deckIndex < this.cards.length; deckIndex++) {
                for(int filterIndex = 0; filterIndex < filter.length; filterIndex++){
                    if(filter[filterIndex].equals(this.cards[deckIndex])){
                        filteredIndexes.add(deckIndex);
                    }
                }
            } 
            if(filteredIndexes.size() == 0){
                System.out.println("out of cards");
            }
            else{
                int mappedSelection = this.selector.nextInt(filteredIndexes.size());
                int selectionIndex = filteredIndexes.get(mappedSelection);
                String oldOwner = this.cards[selectionIndex];
                this.cards[selectionIndex] = newOwner;
                System.out.println(newOwner + " drew a card from " + oldOwner); 
            }
        }
        public void shuffle(String[] filter, String newOwner){
            for (int deckIndex = 0; deckIndex < this.cards.length; deckIndex++) {
                for(int filterIndex = 0; filterIndex < filter.length; filterIndex++){
                    if(filter[filterIndex].equals(this.cards[deckIndex])){
                        this.cards[deckIndex] = newOwner;
                    }
                }
            }
            System.out.println("Shuffled all cards from " + filter[0] + " to " + newOwner); 
        }
    
}
