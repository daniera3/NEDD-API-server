using System;
using System.Collections.Generic;
using System.Text;

namespace NEDDApp.Models
{
    public class User
    {
        private User user = null;
        private String name;
        private User(string name) { this.name = name; }
        public User GetUser(String name)
        {
            if (user == null)
                user = new User(name);
            return user;
        }

    }
}
