
// pub struct ArraySet<T> {
//     arr: Vec<T>
// }

// impl<T> ArraySet<T> where T: std::cmp::PartialEq + Copy {
//     pub fn add(&mut self, element: T) {
//         if self.arr.iter().any(|&i| i == element) {
//             return;
//         } else {
//             self.arr.push(element);
//         }
//     }

//     pub fn new_with_item(item: T) -> ArraySet<T> {
//         let mut arry = Vec::new();

//             arry.push(item);
//         ArraySet{
//             arr: arry
//         }
//     }

//     pub fn delete(&mut self, element: T) {
//         let mut index_to_del: Option<usize> = None;
//         for (i, e) in self.arr.iter().enumerate() {
//             if *e == element {
//                 index_to_del = Some(i);
//                 break;
//             }
//         }
//         if let Some(index) = index_to_del {
//             self.arr.remove(index);
//         } else {
//             return;
//         }
//     }

//     pub fn size(&self) -> usize {
//         self.arr.len()
//     }

//     // Write random pick

//     pub fn get_all(&self) -> Vec<T> {
//         let vec_clone = self.arr.clone();
//         let array: Vec<T> = vec_clone.into_iter()
//             .collect::<Vec<T>>();
//         return array;
//     }

// }
