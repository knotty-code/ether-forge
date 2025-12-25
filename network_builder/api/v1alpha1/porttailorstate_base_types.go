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
// +kubebuilder:resource:path=porttailorstates,scope=Namespaced

// PortTailorState is the Schema for the porttailorstates API
type PortTailorState struct {
	metav1.TypeMeta   `json:",inline"`
	metav1.ObjectMeta `json:"metadata,omitempty"`

	Spec   PortTailorStateSpec   `json:"spec,omitempty"`
	Status PortTailorStateStatus `json:"status,omitempty"`
}

// +kubebuilder:object:root=true

// PortTailorStateList contains a list of PortTailorState
type PortTailorStateList struct {
	metav1.TypeMeta `json:",inline"`
	metav1.ListMeta `json:"metadata,omitempty"`
	Items           []PortTailorState `json:"items"`
}

func init() {
	SchemeBuilder.Register(&PortTailorState{}, &PortTailorStateList{})
}
