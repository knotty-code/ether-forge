/*
Copyright 2025.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

package v1alpha1

import (
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

// +kubebuilder:object:root=true
// +kubebuilder:subresource:status
// +kubebuilder:resource:path=porttailors,scope=Namespaced

// PortTailor is the Schema for the porttailors API
type PortTailor struct {
	metav1.TypeMeta   `json:",inline"`
	metav1.ObjectMeta `json:"metadata,omitempty"`

	Spec   PortTailorSpec   `json:"spec,omitempty"`
	Status PortTailorStatus `json:"status,omitempty"`
}

// +kubebuilder:object:root=true

// PortTailorList contains a list of PortTailor
type PortTailorList struct {
	metav1.TypeMeta `json:",inline"`
	metav1.ListMeta `json:"metadata,omitempty"`
	Items           []PortTailor `json:"items"`
}

func init() {
	SchemeBuilder.Register(&PortTailor{}, &PortTailorList{})
}
