 
                            const currentDate = new Date();
                            let currentMonth = currentDate.getMonth();
                            let currentYear = currentDate.getFullYear();

                            const monthNames = [
                            "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
                            ];

                            function generateCalendar() {
                              const calendarGrid = document.querySelector(".calendar-grid");
                              calendarGrid.innerHTML = "";
                              
                              // Create header for the current month
                              const currentMonthHeader = document.querySelector(".current-month");
                              currentMonthHeader.textContent = monthNames[currentMonth] + " " + currentYear;
                              
                              // Get the first day of the month
                              const firstDay = new Date(currentYear, currentMonth, 1).getDay();
                              
                              // Get the number of days in the month
                              const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();
                              
                              // Generate calendar days
                              for (let i = 0; i < firstDay; i++) {
                                const emptyDay = document.createElement("div");
                                emptyDay.classList.add("calendar-day");
                                calendarGrid.appendChild(emptyDay);
                              }
                              
                              for (let i = 1; i <= daysInMonth; i++) {
                                const calendarDay = document.createElement("div");
                                calendarDay.classList.add("calendar-day");
                                calendarDay.textContent = i;
                                
                                if (currentDate.getMonth() === currentMonth && currentDate.getFullYear() === currentYear && currentDate.getDate() === i) {
                                  calendarDay.classList.add("today");
                                }
                                
                                calendarDay.addEventListener("click", selectDate);
                                
                                calendarGrid.appendChild(calendarDay);
                              }
                            }

                            function selectDate(event) {
                              const selectedDay = document.querySelector(".selected");
                              
                              if (selectedDay) {
                                selectedDay.classList.remove("selected");
                            }

                            event.target.classList.add("selected");
                            }

                            function prevMonth() {
                            if (currentMonth === 0) {
                            currentMonth = 11;
                            currentYear--;
                            } else {
                            currentMonth--;
                            }

                            generateCalendar();
                            }

                            function nextMonth() {
                            if (currentMonth === 11) {
                            currentMonth = 0;
                            currentYear++;
                            } else {
                            currentMonth++;
                            }

                            generateCalendar();
                            }

                            generateCalendar();