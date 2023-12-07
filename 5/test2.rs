fn main() {
	let list = vec![3,76,2,6,8,3,6,0];
	list.sort_by_key(|x| *x);
	println!("{:?}", list);
}
