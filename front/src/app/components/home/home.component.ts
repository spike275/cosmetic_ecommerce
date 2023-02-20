import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';


// Code of Ido and Omer's practice session:
@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {
  selectedFile: File | undefined;
  http: HttpClient
  constructor(http: HttpClient){
    this.http = http
  }
  // onSubmit(){
  //   const formData = new FormData()
  //   formData.append("photo", this.selectedFile!, this.selectedFile!.name)
  //   this.http.post("/api/upload", formData).subscribe(
  //     (response) => console.log(response),
  //     (error) => console.log(error)
  //   )
  // }

//GPT SUGGESTION TO CHANGE THE ONSUBMIT 20.02.2023 21:14:
onSubmit(){
  const formData = new FormData()
  formData.append("photo", this.selectedFile!, this.selectedFile!.name)
  this.http.post("http://localhost:8000/api/upload", formData).subscribe(
    (response) => console.log(response),
    (error) => console.log(error)
  )
}


  onFileSelected(event:any){
    this.selectedFile=event.target.files[0]
  }
}

// //Improved componenet by GPT:

// @Component({
//   selector: 'app-home',
//   templateUrl: './home.component.html',
//   styleUrls: ['./home.component.css']
// })
// export class HomeComponent {
//   selectedFile: File | undefined;
//   http: HttpClient;
//   isUploading = false;
//   errorMessage: string | undefined;
//   successMessage: string | undefined;

//   constructor(http: HttpClient){
//     this.http = http;
//   }

//   onSubmit(){
//     this.errorMessage = undefined;
//     this.successMessage = undefined;
//     this.isUploading = true;

//     const formData = new FormData();
//     formData.append("photo", this.selectedFile!, this.selectedFile!.name);

//     this.http.post("/api/upload", formData).subscribe(
//       (response) => {
//         this.isUploading = false;
//         this.successMessage = "File uploaded successfully!";
//       },
//       (error) => {
//         this.isUploading = false;
//         this.errorMessage = "File upload failed. Please try again later.";
//         console.log(error);
//       }
//     );
//   }


  // //suggested code to check from GPT:
  // // onSubmit(){
  //   const formData = new FormData()
  //   formData.append("photo", this.selectedFile!, this.selectedFile!.name)
  //   console.log(formData.get('photo'));
  //   this.http.post("/api/upload", formData).subscribe(
  //     (response) => console.log(response),
  //     (error) => console.log(error)
  //   )
  // }

//   onFileSelected(event:any){
//     this.selectedFile = event.target.files[0];
//   }
// }





