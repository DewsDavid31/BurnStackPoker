package Game;

import java.util.Random;
import java.util.Scanner;
import java.util.Arrays;
import java.util.ArrayList;


public class Table{
        final int SCREENCLEARLINES = 40;
        final String POTOWNER = "POT";
        final String[] PHASES = {"Bet Phase", "Burn and Swap Phase", "Show Phase","Draw Phase"};
        final String WAITTURN = "Waiting for turn";
        final String PASS = "Passing";
        final String FOLD = "Folded";
        public Deck deck;
        public Player[] players;
        private String[] playerFlags;
        private Random turnSelector;
        private int turnToken;
        private int phase;
        private Scanner keyboardInput;
        public Table(Player[] newPlayers){
            this.deck = new Deck();
            this.players = newPlayers;
            this.playerFlags = new String[newPlayers.length];
            Arrays.fill(this.playerFlags,WAITTURN);
            this.turnSelector = new Random();
            this.turnToken = -1;
            this.phase = 3;
            this.keyboardInput = new Scanner(System.in);
        }
        public int prompt(String message, String[] options){
            for(int choiceIndex = 0; choiceIndex < options.length; choiceIndex++){
                System.out.println(choiceIndex + ": " + options[choiceIndex]);
            }
            System.out.print(message);
            try{
                int selection = keyboardInput.nextInt();
                System.out.println();
                if(selection > options.length || selection < 0){
                    System.out.println("Not a valid selection, try again...");
                    return prompt(message, options);     
                }
                return selection;
            }
            catch(Exception e){
                System.out.println("Input invalid or scanner failed, try again...");
                return prompt(message, options);
            }
        }
        public int promptAmount(String message){
            System.out.print(message);
            try{
                int selection = keyboardInput.nextInt();
                System.out.println();
                if(selection < 0){
                    System.out.println("Not a valid selection, try again...");
                    return promptAmount(message);     
                }
                return selection;
            }
            catch(Exception e){
                System.out.println("Input invalid or scanner failed, try again...");
                return promptAmount(message);
            }
        }

        public void showBoard(){
            for(int clearIndex = 0; clearIndex < SCREENCLEARLINES; clearIndex++){
                System.out.println();
            }
            Boolean isHidden = false;
            System.out.println("Phase: " + PHASES[this.phase]);
            System.out.println("It is " + this.players[this.turnToken].name + "s turn!");
            System.out.println();
            for(int playerIndex = 0; playerIndex < this.players.length; playerIndex++){
                isHidden = false;
                if(playerIndex != this.turnToken){
                    isHidden = true;
                }
                System.out.println(this.players[playerIndex].showHand(isHidden, this.deck));
                System.out.println(this.players[playerIndex].showStack(this.deck));
                System.out.println();
            }
            this.deck.showStack(POTOWNER);
            System.out.println();
        }
        private void pass(int player){
            this.playerFlags[player] = PASS;
        }
        private void fold(int player){
            this.playerFlags[player] = FOLD;
        }
        private void nextTurn(){
            int flagged = 0;
            for(int playerIndex = 0; playerIndex < this.players.length; playerIndex++){
                if(this.playerFlags[playerIndex] != WAITTURN){
                    flagged++;
                }
            }
            if(flagged >= this.players.length){
                if(this.phase == 3){
                    Arrays.fill(this.playerFlags, WAITTURN);
                }
                else{
                    for(int flagIndex = 0; flagIndex < this.playerFlags.length; flagIndex++){
                        if(this.playerFlags[flagIndex].equals(PASS)){
                            this.playerFlags[flagIndex] = WAITTURN;
                        }
                    }
                }
                this.phase++;
                this.phase %= PHASES.length;
            }
            do{
                this.turnToken++;
                this.turnToken %= this.players.length;
            }
            while(this.playerFlags[turnToken] != WAITTURN);
        }
        public void gameplayLoop(){
            while(true){
            if(this.phase == 3){
                for(int playerIndex = 0; playerIndex < this.players.length; playerIndex++){
                    this.players[playerIndex].discard(deck);
                    this.players[playerIndex].draw(deck, 5);
                }
                showBoard();
                String[] options = {"Pass", "Fold"};
                int choice = prompt("Select an action: ",options);
                if(choice == 0){
                    pass(this.turnToken);
                    nextTurn();
                }
                else if(choice == 1){
                    fold(this.turnToken);
                    nextTurn();
                }
            }
            if(this.phase == 2){
                showBoard();
                String[] options = {"Pass", "Fold"};
                int choice = prompt("Select an action: ",options);
                if(choice == 0){
                    pass(this.turnToken);
                    nextTurn();
                }
                else if(choice == 1){
                    fold(this.turnToken);
                    nextTurn();
                }
            }
            if(this.phase == 1){
                showBoard();
                String[] options = {"Pass", "Fold", "Burn", "Swap"};
                int choice = prompt("Select an action: ",options);
                if(choice == 0){
                    pass(this.turnToken);
                    nextTurn();
                }
                else if(choice == 1){
                    fold(this.turnToken);
                    nextTurn();
                }
                else if(choice == 2){
                    int amount = promptAmount("Enter number of cards to burn: ");
                    this.players[this.turnToken].burn(this.deck, amount);
                }
                else if(choice == 3){
                    int amount = promptAmount("Enter index of card in your hand to swap: ");
                    this.players[this.turnToken].swap(this.deck, amount);
                }  
            }
            if(this.phase == 0){
                showBoard();
                String[] options = {"Pass", "Fold", "Bet"};
                int choice = prompt("Select an action: ",options);
                if(choice == 0){
                    pass(this.turnToken);
                    nextTurn();
                }
                else if(choice == 1){
                    fold(this.turnToken);
                    nextTurn();
                }
                else if(choice == 2){
                    int amount = promptAmount("Enter number of cards to bet: ");
                    this.players[this.turnToken].bet(this.deck, amount);
                }
            }
        }
        }
        public void startGame(){
            this.turnToken = turnSelector.nextInt(this.players.length);
            for(int startingBetIndex = 0; startingBetIndex < this.players.length; startingBetIndex++){
                this.players[startingBetIndex].drawBet(deck, false, 10);
            }
            gameplayLoop();
        }
    }

