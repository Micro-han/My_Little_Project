import java.util.*;

/**
	Represents an intelligent agent moving through a particular room.	
	The robot only has one sensor - the ability to get the status of any  
	tile in the environment through the command env.getTileStatus(row, col).
	@author Adam Gaweda, Michael Wollowski
*/

// bfs Node
class Node {
	private int Row, Col;
	private int fa;
	public Node(int row, int col) {
		this.Row = row;
		this.Col = col;
		this.fa = -1;
	}
	public Node(int row, int col, int fa) {
		this.Row = row;
		this.Col = col;
		this.fa = fa;
	}
	public int getRow() {
		return this.Row;
	}
	public int getCol() {
		return this.Col;
	}
	public int getFa() {
		return this.fa;
	}
}

class ANode {
	public int g, h, fa;
	public ANode father;
	public Position point;

	public ANode(Position point, Position epoint, int g) {
		this.point = point;
		this.g = g;
		this.h = (Math.abs(epoint.getRow() - point.getRow()) + Math.abs(epoint.getCol() - point.getCol())) * 10;
	}

	public int compareTo(ANode o) {
		if (o == null) return -1;
		if (this.g + this.h < o.g + o.h) return -1;
		if (this.g + this.h > o.g + o.h) return 1;
		return 0;
	}
}

public class Robot {
	private Environment env;
	private int posRow;
	private int posCol;
	private LinkedList<Action> path;
	private boolean pathFound;
	private int openCount;
	private int pathLength;
	private int cnt;
	
	/**
	    Initializes a Robot on a specific tile in the environment. 
	*/
	
	public Robot (Environment env, int posRow, int posCol) {
		this.env = env;
		this.posRow = posRow;
		this.posCol = posCol;
		this.path = new LinkedList<>();
		this.pathFound = false;
		this.openCount = 0;
		this.pathLength = 0;
		this.cnt = 0;
	}
	
	public void init() {
		/**
		 * change this to change method
		 **/
		// bfs();
		// bfsM();
		// astar();
		astarM();
	}
	
	public boolean getPathFound(){
		return this.pathFound;
	}
	
	public long getOpenCount(){
		return this.openCount;
	}
	
	public int getPathLength(){
		return this.pathLength;
	}
	
	public void resetOpenCount() {
		this.openCount = 0;
	}
	
	public int getPosRow() { return posRow; }
	public int getPosCol() { return posCol; }
	public void incPosRow() { posRow++; }
	public void decPosRow() { posRow--; }
	public void incPosCol() { posCol++; }
    public void decPosCol() { posCol--; }
	
	/**
	   Returns the next action to be taken by the robot. A support function 
	   that processes the path LinkedList that has been populates by the
	   search functions.
	*/
	public Action getAction () {
		//TODO: Implement this method
		if(this.cnt < this.pathLength) {
			Action now_act = this.path.get(this.cnt);
			this.cnt = this.cnt + 1;
			return now_act;
		} else return Action.DO_NOTHING;
	}
	
	/** 
	 * This method implements breadth-first search. It populates the path LinkedList
	 * and sets pathFound to true, if a path has been found. IMPORTANT: This method 
	 * increases the openCount field every time your code adds a node to the open
	 * data structure, i.e. the queue or priorityQueue
	 * 
	 */
	public void bfs() {
		//TODO: Implement this method
		int cols = this.env.getCols(), rows = this.env.getRows();
		int ed_col = this.env.getTargetCol(), ed_row = this.env.getTargetRow();
		// RIGHT, LEFT, DOWN, UP
		int [][] dis = {{0,1}, {0,-1}, {1,0}, {-1,0}};
		int [][] vis = new int [rows][cols];
		int tmp = 0;
		Node [][] tmap = new Node [rows][cols];
		Action[] ans = new Action[cols * rows];
		Queue<Position> q = new LinkedList();
		q.offer(new Position(this.posRow, this.posCol));
		while(!q.isEmpty()) {
			Position point = q.poll();
			vis[point.getRow()][point.getCol()] = 1;
			this.openCount += 1;
			for(int i = 0; i < 4; i++) {
				int new_col = point.getCol() + dis[i][1];
				int new_row = point.getRow() + dis[i][0];
				if(this.env.validPos(new_row, new_col) && vis[new_row][new_col] == 0) {
					tmap[new_row][new_col] = new Node(new_row, new_col, i);
					if(ed_col == new_col && ed_row == new_row) {
						this.pathFound = true;
						int final_row = ed_row, final_col = ed_col;
						while(true) {
							int n_act = tmap[final_row][final_col].getFa();
							switch (n_act) {
								case 0:{ans[tmp] = Action.MOVE_RIGHT;tmp = tmp + 1;final_col = final_col - 1;break;}
								case 1:{ans[tmp] = Action.MOVE_LEFT;tmp = tmp + 1;final_col = final_col + 1;break;}
								case 2:{ans[tmp] = Action.MOVE_DOWN;tmp = tmp + 1;final_row = final_row - 1;break;}
								case 3: {ans[tmp] = Action.MOVE_UP;tmp = tmp + 1;final_row = final_row + 1;break;}
							}

							if(final_row == this.posRow && final_col == this.posCol) break;
						}
						this.pathLength = tmp;
						for(int j = 0; j < tmp; j++) this.path.add(ans[tmp - j - 1]);
						break;
					} else {
						vis[new_row][new_col] = 1;
						q.offer(new Position(new_row, new_col));
					}
				}
			}
			if(this.pathFound) break;
		}
		if(!this.pathFound) {
			System.out.println(this.openCount);
			System.out.println("Can not find!");
		}
	}
	

	/** 
	 * This method implements breadth-first search for maps with multiple targets.
	 * It populates the path LinkedList
	 * and sets pathFound to true, if a path has been found. IMPORTANT: This method 
	 * increases the openCount field every time your code adds a node to the open
	 * data structure, i.e. the queue or priorityQueue
	 * 
	 */
	public Position bfs2(int[][] targets, int row, int col) {
		int cols = this.env.getCols(), rows = this.env.getRows();
		// RIGHT, LEFT, DOWN, UP
		int [][] dis = {{0,1}, {0,-1}, {1,0}, {-1,0}};
		int [][] vis = new int [rows][cols];
		int tmp = 0;
		Action[] ans = new Action[rows * cols];
		Queue<Position> q = new LinkedList<>();
		q.offer(new Position(row, col));
		Node [][] tmap = new Node [rows][cols];
		while(!q.isEmpty()) {
			Position point = q.poll();
			vis[point.getRow()][point.getCol()] = 1;
			this.openCount += 1;
			for(int i = 0; i < 4; i++) {
				int new_row = point.getRow() + dis[i][0];
				int new_col = point.getCol() + dis[i][1];
				if(this.env.validPos(new_row, new_col) && vis[new_row][new_col] == 0) {
					tmap[new_row][new_col] = new Node(new_row, new_col, i);
					if(targets[new_row][new_col] == 3) {
						targets[new_row][new_col] = 0;
						int final_row = new_row, final_col = new_col;
						while(true) {
							int n_act = tmap[final_row][final_col].getFa();
							switch (n_act) {
								case 0:{ans[tmp] = Action.MOVE_RIGHT;tmp = tmp + 1;final_col = final_col - 1;break;}
								case 1:{ans[tmp] = Action.MOVE_LEFT;tmp = tmp + 1;final_col = final_col + 1;break;}
								case 2:{ans[tmp] = Action.MOVE_DOWN;tmp = tmp + 1;final_row = final_row - 1;break;}
								case 3: {ans[tmp] = Action.MOVE_UP;tmp = tmp + 1;final_row = final_row + 1;break;}
							}
							if(final_row == row && final_col == col) break;
						}
						for(int j = 0; j < tmp; j++) this.path.add(ans[tmp - j - 1]);
						return new Position(new_row, new_col);
					} else {
						vis[new_row][new_col] = 1;
						q.offer(new Position(new_row, new_col));
					}
				}
			}
		}
		System.out.println(1);
		return null;
	}
	public void bfsM() {
		//TODO: Implement this method
		int cols = this.env.getCols(), rows = this.env.getRows();
		LinkedList<Position> eds = this.env.getTargets();
		int[][] targets = new int[rows][cols];
		int target_num = 0;
		for (int i = 0; i < eds.size(); i++) {
			int x = eds.get(i).getRow(), y = eds.get(i).getCol();
			targets[x][y] = 3;
		}
		int st_row = this.posRow, st_col = this.posCol;

		while (target_num < eds.size()) {
			target_num += 1;
			Position p = bfs2(targets, st_row, st_col);
			st_col = p.getCol();
			st_row = p.getRow();
		}
		int flag = 0;
		for(int i = 0; i < rows; i++)
			for(int j = 0; j < cols; j++) {
				if(targets[i][j] == 3) flag = 1;
			}
		if(flag == 0) {
			this.pathFound = true;
			this.pathLength = path.size();
		}
//		System.out.println(this.path.size());
//		System.out.println(pathLength);
//		for(int i = 0; i < this.path.size(); i++) System.out.println(this.path.get(i));
		//for(int i = 0; i < path.size(); i++) System.out.println(path.get(i));
	}



	/** 
	 * This method implements A* search. It populates the path LinkedList
	 * and sets pathFound to true, if a path has been found. IMPORTANT: This method 
	 * increases the openCount field every time your code adds a node to the open
	 * data structure, i.e. the queue or priorityQueue
	 * 
	 */

	public ANode pointInCloseList(ArrayList<ANode> close_lst, Position position) {
		for(ANode node : close_lst)
			if(node.point.getCol() == position.getCol() && node.point.getRow() == position.getRow()) return node;
		return null;
	}

	public ANode pointInOpenList(PriorityQueue<ANode> open_lst, Position position) {
		for(ANode node : open_lst)
			if(node.point.getRow() == position.getRow() && node.point.getCol() == position.getCol()) return node;
		return null;
	}

	public void astar() {
		//TODO: Implement this method
		int cols = this.env.getCols(), rows = this.env.getRows();
		int ed_col = this.env.getTargetCol(), ed_row = this.env.getTargetRow();
		int [][] dis = {{0,1}, {0,-1}, {1,0}, {-1,0}};
		PriorityQueue<ANode> open_lst = new PriorityQueue<>(ANode::compareTo);
		ArrayList<ANode> close_lst = new ArrayList<>();
		Position snode = new Position(this.posRow, this.posCol);
		Position enode = new Position(ed_row, ed_col);
		ANode startNode = new ANode(snode, enode, 0);
		open_lst.add(startNode);
		while(!open_lst.isEmpty()) {
			this.openCount += 1;
			ANode minNode = open_lst.poll();
			close_lst.add(minNode);
			for(int i = 0; i < 4; i++) {
				int new_row = minNode.point.getRow() + dis[i][0], new_col = minNode.point.getCol() + dis[i][1];
				Position currentPoint = new Position(new_row, new_col);

				if(this.env.validPos(new_row, new_col) && pointInCloseList(close_lst, currentPoint) == null) {
					ANode cnode = pointInOpenList(open_lst, currentPoint);
					if(cnode == null) {
						cnode = new ANode(currentPoint, enode, minNode.g + 10);
						cnode.father = minNode;
						cnode.fa = i;
						open_lst.add(cnode);
					} else {
						if(minNode.g + 10 < cnode.g) {
							cnode.g = minNode.g + 10;
							cnode.father = minNode;
							cnode.fa = i;
						}
					}
				}
			}
			ANode node = pointInCloseList(close_lst, enode);
			if(node != null) {
				this.pathFound = true;
				Action[] ans = new Action[rows * cols];
				int tmp = 0;
				while(true) {
					if(node.father != null) {
						int n_act = node.fa;
						switch (n_act) {
							case 0:{ans[tmp] = Action.MOVE_RIGHT;tmp = tmp + 1;break;}
							case 1:{ans[tmp] = Action.MOVE_LEFT;tmp = tmp + 1;break;}
							case 2:{ans[tmp] = Action.MOVE_DOWN;tmp = tmp + 1;break;}
							case 3: {ans[tmp] = Action.MOVE_UP;tmp = tmp + 1;break;}
						}
						node = node.father;
					} else {
						for(int i = 0; i < tmp; i++) this.path.add(ans[tmp - i - 1]);
						this.pathLength = tmp;
						break;
					}
				}
			}
		}
		if(!this.pathFound) {
			System.out.println(this.openCount);
			System.out.println("Can not found");
		}
	}

	
	/** 
	 * This method implements A* search for maps with multiple targets. It 
	 * populates the path LinkedList
	 * and sets pathFound to true, if a path has been found. IMPORTANT: This method 
	 * increases the openCount field every time your code adds a node to the open
	 * data structure, i.e. the queue or priorityQueue
	 * 
	 */
	public void astarM() {
		//TODO: Implement this method
		int rows = this.env.getRows(), cols = this.env.getCols();
		LinkedList<Position> eds = this.env.getTargets();
		int[][] dis = {{0, 1}, {0, -1}, {1, 0}, {-1, 0}};

		Position snode = new Position(this.posRow, this.posCol);
		// everytime choose a new nearby endnode
		int ed_up = eds.size(), ed_cnt = 0;
		int[] vis = new int[ed_up];

		PriorityQueue<ANode> open_lst = new PriorityQueue<>(ANode::compareTo);
		ArrayList<ANode> close_lst = new ArrayList<>();
		PriorityQueue<ANode> choose_lst = new PriorityQueue<>(ANode::compareTo);

		while (true) {
			boolean tmpflag = false;

			open_lst.clear();
			close_lst.clear();
			choose_lst.clear();

			for (int i = 0; i < eds.size(); i++)
				if(vis[i] == 0)choose_lst.add(new ANode(eds.get(i), snode, 0));
			ANode choose_min_node = choose_lst.poll();
			int eds_index = 0;
			for (int i = 0; i < eds.size(); i++)
				if (eds.get(i).getCol() == choose_min_node.point.getCol() && eds.get(i).getRow() == choose_min_node.point.getRow()) {
					eds_index = i;
					break;
				}
			Position enode = eds.get(eds_index);
			vis[eds_index] = 1;
			ANode startNode = new ANode(snode, enode, 0);
			open_lst.add(startNode);
			while (!open_lst.isEmpty()) {
				this.openCount += 1;
				ANode minNode = open_lst.poll();
				close_lst.add(minNode);
				for (int i = 0; i < 4; i++) {
					int new_row = minNode.point.getRow() + dis[i][0], new_col = minNode.point.getCol() + dis[i][1];
					Position currentPoint = new Position(new_row, new_col);
					if (this.env.validPos(new_row, new_col) && pointInCloseList(close_lst, currentPoint) == null) {
						ANode cnode = pointInOpenList(open_lst, currentPoint);
						if (cnode == null) {
							cnode = new ANode(currentPoint, enode, minNode.g + 10);
							cnode.father = minNode;
							cnode.fa = i;
							open_lst.add(cnode);
						} else {
							if (minNode.g + 10 < cnode.g) {
								cnode.g = minNode.g + 10;
								cnode.father = minNode;
								cnode.fa = i;
							}
						}
					}
				}
				ANode node = pointInCloseList(close_lst, enode);
				if (node != null) {
					tmpflag = true;
					Action[] ans = new Action[rows * cols];
					int tmp = 0;
					while (true) {
						if (node.father != null) {
							int n_act = node.fa;
							switch (n_act) {
								case 0: {
									ans[tmp] = Action.MOVE_RIGHT;
									tmp = tmp + 1;
									break;
								}
								case 1: {
									ans[tmp] = Action.MOVE_LEFT;
									tmp = tmp + 1;
									break;
								}
								case 2: {
									ans[tmp] = Action.MOVE_DOWN;
									tmp = tmp + 1;
									break;
								}
								case 3: {
									ans[tmp] = Action.MOVE_UP;
									tmp = tmp + 1;
									break;
								}
							}
							node = node.father;
						} else {
							for (int i = 0; i < tmp; i++) this.path.add(ans[tmp - i - 1]);
							this.pathLength += tmp;
							break;
						}
					}
				}
				if(tmpflag) break;
			}

			if(tmpflag) {
				ed_cnt += 1;
				snode = enode;
			} else break;

			if(ed_cnt == ed_up) {
				this.pathFound = true;
				break;
			}
		}

		if(!this.pathFound) {
			System.out.println(this.openCount);
			System.out.println("Can not found");
		}

	}
}