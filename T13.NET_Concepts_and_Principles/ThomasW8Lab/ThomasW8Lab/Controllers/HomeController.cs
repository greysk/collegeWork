using Microsoft.AspNetCore.Mvc;
using System.Security.Policy;
using ThomasW8Lab.Models;

namespace ThomasW8Lab.Controllers
{
    public class HomeController : Controller
    {
        public IActionResult Index()
        {
            ViewBag.Title = "Home";
            return View();
        }
        public IActionResult About()
        {
            ViewBag.Title = "About";
            return View();
        }
        public IActionResult Contact()
        {
            ViewBag.Title = "Contact";
            return View();
        }
        public IActionResult Links()
        {
            ViewBag.Title = "Links";
            LinkModel myURL = new LinkModel
            {
                LinkText = "Create web apps and services with ASP.NET Core, minimal API, and .NET | Microsoft Learn",
                URL = "https://learn.microsoft.com/en-us/training/paths/aspnet-core-minimal-api/",
                ReferPolicy = "no-referrer",
                Category = "Course/Lesson"
            };
            return View(myURL);
        }
    }
}
